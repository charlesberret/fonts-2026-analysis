#!/usr/bin/env python
"""Run CSS-side font queries against fonts_2026.pruned_css + root_pages.

Requires pruned_css materialize to succeed first.

Usage:
  export CLOUDSDK_CORE_DISABLE_PROMPTS=1
  python execute_css_materialized.py              # dry-run
  python execute_css_materialized.py --no-dry-run
  python execute_css_materialized.py --no-dry-run performance/styles_font_display.sql
"""

from __future__ import annotations

import argparse
import multiprocessing
import os
import re
import sys
from pathlib import Path

import google.auth  # pylint: disable=import-error
import pandas as pd  # pylint: disable=import-error
from google.cloud import bigquery  # pylint: disable=import-error

os.environ.setdefault("CLOUDSDK_CORE_DISABLE_PROMPTS", "1")

PROJECT_ID = "fonts-data-analysis"
DATASET_ID = "fonts_2026"
PRUNED_CSS = f"`{PROJECT_ID}.{DATASET_ID}.pruned_css`"
ROOT_PAGES = f"`{PROJECT_ID}.{DATASET_ID}.root_pages`"
FONT_REQUESTS = f"`{PROJECT_ID}.{DATASET_ID}.font_requests`"

QUERY_PARAMETERS = [
    bigquery.ScalarQueryParameter("date", "DATE", "2026-07-01"),
    bigquery.ArrayQueryParameter("dates", "DATE", ["2026-07-01"]),
    bigquery.ScalarQueryParameter("precision", "INT64", 4),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="*", default=["*/*.sql"])
    parser.add_argument("--no-dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--workers", type=int, default=1
    )  # serial default: CSS jobs are heavy
    args = parser.parse_args()

    paths = sorted(
        {
            p
            for pattern in args.path
            for p in Path(".").glob(pattern)
            if p.suffix == ".sql" and _is_eligible(p)
        }
    )
    if not paths:
        print("No eligible CSS queries found.")
        sys.exit(1)

    print(f"Eligible CSS queries: {len(paths)}")
    print(f"Mode: {'EXECUTE' if args.no_dry_run else 'DRY-RUN'}")
    print()

    width = max(len(str(p)) for p in paths) + 1
    tasks = [
        {"path": p, "dry_run": not args.no_dry_run, "force": args.force}
        for p in paths
    ]

    if args.workers <= 1:
        results = [_process(t) for t in tasks]
    else:
        with multiprocessing.Pool(args.workers) as pool:
            results = list(pool.imap_unordered(_process, tasks))

    ok = fail = skip = 0
    for result in sorted(results, key=lambda r: str(r["task"]["path"])):
        path = result["task"]["path"]
        if result.get("skipped"):
            print(f"{str(path).ljust(width)}: skipped ({result['skipped']})")
            skip += 1
        elif result["failures"]:
            msg = result["failures"][0].splitlines()[0]
            print(f"{str(path).ljust(width)}: FAIL {msg}")
            fail += 1
        else:
            print(f"{str(path).ljust(width)}: {result['successes'][0]}")
            ok += 1

    print()
    print(f"=== {ok} ok, {fail} fail, {skip} skipped ===")
    sys.exit(1 if fail else 0)


def _is_eligible(path: Path) -> bool:
    if path.parts[0] == "materialize":
        return False
    text = path.read_text()
    return "crawl.parsed_css" in text or "parsed_css" in text


def _process(task: dict) -> dict:
    result = {"task": task, "failures": [], "successes": [], "skipped": None}
    path: Path = task["path"]
    csv_path = path.with_suffix(".csv")

    if csv_path.exists() and not task["dry_run"] and not task.get("force"):
        result["skipped"] = "csv exists"
        return result

    try:
        raw = _query_read(path)
        sql = rewrite_to_pruned(raw)
        if task["dry_run"]:
            tb = _estimate(sql)
            result["successes"].append(f"estimated {tb:6.3f} TB  ~${tb * 5:6.2f}")
        else:
            data = _read(sql)
            data.to_csv(csv_path, index=False)
            table = f"{path.parent.name}__{path.stem}"
            _load(data, table)
            result["successes"].append(
                f"wrote {csv_path} + {DATASET_ID}.{table} ({len(data)} rows)"
            )
    except Exception as error:  # pylint: disable=broad-except
        result["failures"].append(str(error))
    return result


def rewrite_to_pruned(sql: str) -> str:
    out = sql
    out = out.replace("`httparchive.crawl.parsed_css`", PRUNED_CSS)
    out = out.replace("httparchive.crawl.parsed_css", f"{PROJECT_ID}.{DATASET_ID}.pruned_css")
    # Page totals / non-font request scans → root_pages when appropriate
    out = out.replace("`httparchive.crawl.requests`", FONT_REQUESTS)
    out = out.replace("httparchive.crawl.requests", f"{PROJECT_ID}.{DATASET_ID}.font_requests")
    out = _retarget_page_totals(out)
    return out


def _retarget_page_totals(sql: str) -> str:
    pattern = re.compile(
        r"(pages\s+AS\s*\(\s*"
        r"SELECT[\s\S]*?"
        r"FROM\s+)"
        + re.escape(FONT_REQUESTS)
        + r"(\s+WHERE[\s\S]*?\))",
        re.IGNORECASE,
    )

    def repl(match: re.Match) -> str:
        head, tail = match.group(1), match.group(2)
        if re.search(r"type\s*=\s*['\"]font['\"]", tail, re.I):
            return match.group(0)
        return head + ROOT_PAGES + tail

    return pattern.sub(repl, sql)


def _query_read(path: Path) -> str:
    lines = []
    for line in path.read_text().splitlines():
        match = re.search(r"^-- INCLUDE .*/([^/]+)\.sql$", line)
        if match:
            (name,) = match.groups()
            lines.extend(Path(f"{name}.sql").read_text().splitlines())
        else:
            lines.append(line)
    return "\n".join(lines)


def _estimate(sql: str) -> float:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    config = bigquery.QueryJobConfig(
        query_parameters=QUERY_PARAMETERS,
        use_query_cache=False,
        dry_run=True,
    )
    job = client.query(sql, job_config=config)
    return (job.total_bytes_processed or 0) / 1024**4


def _read(sql: str) -> pd.DataFrame:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    config = bigquery.QueryJobConfig(
        query_parameters=QUERY_PARAMETERS,
        use_query_cache=True,
    )
    job = client.query(sql, job_config=config)
    return job.to_dataframe()


def _load(data: pd.DataFrame, table: str) -> None:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table}"
    config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(data, table_id, job_config=config)
    job.result()


if __name__ == "__main__":
    main()
