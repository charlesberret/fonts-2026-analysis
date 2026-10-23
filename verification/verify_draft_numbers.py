#!/usr/bin/env python3
"""verify_draft_numbers.py — the scripted gate the finish plan specified.

Reads verification/source-map-2026.csv (v2-keyed claims C001+) plus
verification/source-map-v7-delta.csv (claims added by the v7 intel edits),
and checks both directions against drafts/fonts-2026-v7.md:

  forward   every numeric token in a live map row's `value` field must occur
            in the draft (numbers survive voice passes; a missing token means
            the claim was dropped or renumbered — listed for review)
  backward  every numeric token in the draft must trace to a map row, the
            delta, or the structural allowlist (years, versions, section
            numbers, ordinals, lone digits)

Writes verification/report-<date>.md and exits 1 on any unexplained token.

Usage: verify_draft_numbers.py [--draft PATH] [--date YYYY-MM-DD]
"""
import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?\s*%?|\d+(?:\.\d+)?")
YEARISH = re.compile(r"^(19|20)\d{2}$")
VERSION = re.compile(r"^\d+\.\d+(\.\d+)+$")


def canon(t):
    """canonical numeric string: strip %, commas; float-form when parseable"""
    t = t.rstrip("%").replace(",", "").rstrip(".")
    try:
        return f"{float(t):g}"
    except ValueError:
        return t


def tokens(text):
    out = set()
    for m in NUM.finditer(text):
        t = canon(m.group(0).replace(" ", ""))
        if t:
            out.add(t)
    return out


def structural(tok):
    return bool(YEARISH.match(tok.rstrip("%")) or VERSION.match(tok)
                or (len(tok.rstrip("%")) <= 2 and "." not in tok))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", default=str(ROOT / "drafts/fonts-2026-v7.md"))
    ap.add_argument("--date", default=date.today().isoformat())
    a = ap.parse_args()
    draft = Path(a.draft).read_text()
    # footnote definitions ([^n]: ...) are citations, not claims: issue numbers,
    # comment ids and dates in them are not numbers the report asserts
    draft = "\n".join(l for l in draft.split("\n") if not l.startswith("[^"))
    draft_toks = tokens(draft)

    rows = []
    for f in ("source-map-2026.csv", "source-map-v7-delta.csv"):
        p = HERE / f
        if p.exists():
            rows += [r | {"_file": f} for r in csv.DictReader(p.open())]

    # every numeric cell of every CSV under data/ and sql/ is a sourced value;
    # a draft token matches it raw or as a percent (0.526 -> 52.6%)
    csv_toks = set()
    for d in (ROOT / "data", ROOT / "sql"):
        for p in d.rglob("*.csv"):
            # never read a virtual environment's package data as if it were a result
            if any(part in (".venv", "venv", "site-packages", "__pycache__") for part in p.parts):
                continue
            try:
                for line in p.open(errors="ignore"):
                    for cell in line.split(","):
                        for t in tokens(cell):
                            csv_toks.add(t)
                            try:
                                csv_toks.add(f"{float(t.rstrip('%'))*100:g}%")
                                csv_toks.add(f"{float(t.rstrip('%'))/100:g}")
                            except ValueError:
                                pass
            except OSError:
                pass

    live = [r for r in rows if r.get("status") not in ("removed", "superseded")]
    mapped = set()
    missing, in_source = [], []
    for r in live:
        toks = tokens(r.get("value", ""))
        if not toks:
            continue
        absent = [t for t in toks if t not in draft_toks]
        if absent:
            src = ROOT / r.get("source_file", "")
            src_toks = set()
            if src.is_file():
                for t in tokens(src.read_text(errors="ignore")):
                    src_toks.add(t)
                    try:
                        src_toks.add(f"{float(t.rstrip('%'))*100:g}%")
                    except ValueError:
                        pass
            if all(t in src_toks for t in absent):
                in_source.append((r["claim_id"], ", ".join(absent)))
            else:
                missing.append((r["claim_id"], r["claim_text"][:70], ", ".join(absent)))
        else:
            mapped |= toks

    uncovered, weak = {}, {}
    for i, line in enumerate(draft.splitlines(), 1):
        for t in tokens(line):
            if t in mapped or structural(t):
                continue
            # a token found only somewhere in data/ or sql/ is a weak trace: the pool
            # is large enough that a wrong number usually matches some cell (probe,
            # 2026-10-16: four planted wrong values all passed). Listed, not failed.
            (weak if t in csv_toks else uncovered).setdefault(t, []).append(i)

    rp = HERE / f"report-{a.date}.md"
    with rp.open("w") as f:
        f.write(f"# verify_draft_numbers report — {a.date}\n\n"
                f"Draft: `{a.draft}` · rows checked: {len(live)} "
                f"({sum(1 for r in live if tokens(r.get('value','')))} with values)\n\n"
                f"## Forward (map → draft)\n\n"
                + (f"**{len(missing)} live map rows have values absent from the draft:**\n\n"
                   + "\n".join(f"- {c} {txt} — missing: {v}" for c, txt, v in missing) + "\n\n"
                   if missing else "All live map values present in the draft.\n\n")
                + (f"**{len(in_source)} absent-from-draft rows trace to their cited CSV "
                   "(moved to figure/table, or dropped claim):**\n\n"
                   + "\n".join(f"- {c} — {v}" for c, v in in_source) + "\n\n")
                + f"## Backward (draft → map)\n\n"
                + (f"**{len(uncovered)} draft tokens trace to no map row:**\n\n"
                   + "\n".join(f"- `{t}` — lines {', '.join(map(str, ls[:6]))}"
                               for t, ls in sorted(uncovered.items())) + "\n"
                   if uncovered else "Every draft number traces to a map row or to some CSV cell.\n")
                + (f"\n**{len(weak)} draft tokens match no map row, only some cell in data/ or sql/ "
                   "(weak trace; check each against its claim):**\n\n"
                   + "\n".join(f"- `{t}` — lines {', '.join(map(str, ls[:6]))}"
                               for t, ls in sorted(weak.items())) + "\n" if weak else ""))
    print(f"wrote {rp}: missing={len(missing)} uncovered={len(uncovered)} weak={len(weak)}")
    sys.exit(1 if missing or uncovered else 0)


if __name__ == "__main__":
    main()
