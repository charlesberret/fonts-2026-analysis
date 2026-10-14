#!/usr/bin/env python
"""Render figures for "Fonts on the Web 2026".

Usage:
    python render.py F1 [F2 ...]
    python render.py --all

Each figure is one function: read its CSV with pandas, draw through grammar.py
(the Specimen frame, A5 Kettle scheme),
save both out/fNN-<slug>.svg (live text) and out/fNN-<slug>.png (1600px wide).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import grammar as g

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "multi-year"
SQL = HERE.parent / "sql"


class AnchorMismatch(Exception):
    """A CSV value drifted from the value the chapter text is anchored to."""


def _anchor(figure, what, actual, expected, tol=0.2, unit="pp"):
    """Refuse to draw a figure whose data no longer matches the prose."""
    delta = abs(float(actual) - float(expected))
    if delta > tol:
        raise AnchorMismatch(
            f"{figure}: {what} reads {actual:,.2f} but the brief anchors it at "
            f"{expected:,.2f} — off by {delta:,.2f}{unit}, tolerance "
            f"{tol}{unit}. Not drawing; check the source query."
        )
    return float(actual)


def _annual_series(csv_name, value_col="proportion"):
    """Load a year x client CSV as percentages, one July row per year.

    Returns {client: DataFrame(year, value)} sorted by year.
    """
    df = pd.read_csv(DATA / csv_name)
    for required in ("year", "client", value_col):
        if required not in df.columns:
            raise ValueError(
                f"{csv_name}: expected column {required!r}, found {list(df.columns)}"
            )

    # Prefer July snapshots when the source carries multiple rows per year.
    if "crawl_date" in df.columns:
        dates = pd.to_datetime(df["crawl_date"], errors="coerce")
        july = df[dates.dt.month == 7]
        if not july.empty:
            counts = df.groupby(["year", "client"]).size()
            if (counts > 1).any():
                df = july
        df = df.assign(_d=dates).sort_values("_d").drop_duplicates(
            ["year", "client"], keep="last"
        )

    df = df.copy()
    df["value"] = df[value_col].astype(float) * 100.0
    return {
        client: part.sort_values("year")[["year", "value"]].reset_index(drop=True)
        for client, part in df.groupby("client")
    }


def _client_lines(ax, series, label_dx, markers=False, front="mobile", where="input"):
    """Desktop (cobalt) and mobile (cerise) lines with end dots and direct labels.

    Set the y limits before calling: label spacing is measured in pixels.
    Returns {client: latest value}.
    """
    missing = {"desktop", "mobile"} - set(series)
    if missing:
        raise ValueError(f"{where}: missing client series {sorted(missing)}")
    latest, ends = {}, []
    for client, label in (("desktop", "Desktop"), ("mobile", "Mobile")):
        data = series[client]
        g.line(ax, data["year"], data["value"], client, markers=markers)
        last = data.iloc[-1]
        g.end_dot(ax, float(last["year"]), float(last["value"]), client, front=client == front)
        latest[client] = float(last["value"])
        ends.append((float(last["year"]), float(last["value"]), f"{label} {last['value']:.1f}"))
        print(f"  {client}: {int(last['year'])} = {last['value']:.1f}%")
    g.end_labels(ax, ends, dx=label_dx)
    return latest


def f1():
    """F1 - Pages requesting at least one web font, 2011-2026."""
    series = _annual_series("chart_font_usage_annual.csv")
    fig, ax = g.new_figure(
        1, "Adoption",
        "Pages requesting at least one web font, 2011–2026",
        "Share of root pages; desktop and mobile crawled separately",
        "pages",
        client_series=["desktop", "mobile"],
    )
    g.percent_axis(ax, top=100, step=20)
    g.unit_label(ax, "percent of root pages")
    latest = _client_lines(ax, series, label_dx=0.55, front="desktop", where="chart_font_usage_annual.csv")
    years = list(series["desktop"]["year"])
    g.year_axis(ax, years, step=3)
    ax.set_xlim(2010.4, 2029.6)
    first = float(series["desktop"].iloc[0]["value"])
    g.margin_number(
        fig, f"{latest['desktop']:.1f}", "%",
        f"of desktop root pages requested at least one web font in July 2026; "
        f"mobile {latest['mobile']:.1f}%.",
        note=f"Up from {first:.1f}% of desktop pages in 2011, the first full year of data.",
    )
    g.source_note(fig, "Source: HTTP Archive root pages, July crawls (July 1 or July 15 each year; "
                       "2026 = July 1, 2026 crawl). Denominator: root pages per client.")
    return g.save_figure(fig, 1, "font-usage-over-time")


def f2():
    """F2 - Pages using at least one variable font, 2019-2026."""
    series = _annual_series("chart_variable_fonts.csv")
    fig, ax = g.new_figure(
        2, "Variable fonts",
        "Pages loading at least one variable font, 2019–2026",
        "Share of root pages; desktop and mobile crawled separately",
        "pages",
        client_series=["desktop", "mobile"],
    )
    g.percent_axis(ax, top=60, step=10)
    g.unit_label(ax, "percent of root pages")
    latest = _client_lines(ax, series, label_dx=0.22, where="chart_variable_fonts.csv")
    g.year_axis(ax, range(2019, 2027))
    ax.set_xlim(2018.7, 2027.35)
    prior = float(series["desktop"].set_index("year")["value"].loc[2025])
    g.margin_number(
        fig, f"{latest['mobile']:.1f}", "%",
        f"of mobile root pages loaded at least one variable font in July 2026; "
        f"desktop {latest['desktop']:.1f}%.",
        note=f"Desktop gained {latest['desktop'] - prior:.1f} points in a year, "
             "the largest rise since 2022.",
    )
    g.source_note(fig, "Source: HTTP Archive root pages, mid-year crawls (July; Sept. 2020, June 2022; "
                       "2021 via the 2022 chapter). Denominator: root pages per client.")
    return g.save_figure(fig, 2, "variable-font-adoption")


# --------------------------------------------------------------------------
# Column helpers (shared by F4/F6/F7/F8)
# --------------------------------------------------------------------------


def _desktop_frame(csv_name, key_col, value_col="proportion", years=None, keys=None):
    """Desktop rows of a year x category CSV as a year-indexed percentage table."""
    df = pd.read_csv(DATA / csv_name)
    for required in ("year", "client", key_col, value_col):
        if required not in df.columns:
            raise ValueError(
                f"{csv_name}: expected column {required!r}, found {list(df.columns)}"
            )
    data = df[df["client"] == "desktop"]
    if keys is not None:
        data = data[data[key_col].isin(keys)]
    if years is not None:
        data = data[data["year"].isin(years)]
        found = sorted(data["year"].unique())
        if found != sorted(years):
            raise ValueError(f"{csv_name}: wanted years {years}, found {found}")
    table = data.pivot(index="year", columns=key_col, values=value_col) * 100.0
    return table.sort_index()


def _year_columns(ax, years, pad=0.45):
    x = list(range(len(years)))
    g.category_axis(ax, x, [str(y) for y in years])
    ax.set_xlim(-0.55, len(years) - pad)
    return x


def _category_columns(ax, labels):
    x = list(range(len(labels)))
    g.category_axis(ax, x, labels)
    ax.set_xlim(-0.55, len(labels) - 0.45)
    return x


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------


def f4():
    """F4 - How desktop pages combine Google Fonts and self-hosting, 2022-2026."""
    years = [2022, 2023, 2024, 2025, 2026]
    table = _desktop_frame("chart_service_combos.csv", "services", years=years)

    combos = [
        ("Google, self-hosted", "Hybrid (Google + self-hosted)", g.SERIES[0]),
        ("self-hosted", "Self-hosted only", g.SERIES[1]),
        ("Google", "Google only", g.SERIES[2]),
    ]
    for key, _, _ in combos:
        if key not in table.columns:
            raise ValueError(
                f"chart_service_combos.csv: no {key!r} column; got "
                f"{list(table.columns)}"
            )

    print(f"  2026 desktop: " + ", ".join(
        f"{label} {table.loc[2026, key]:.1f}%" for key, label, _ in combos
    ))
    hybrid, selfonly = combos[0][0], combos[1][0]
    gap22 = table.loc[2022, hybrid] - table.loc[2022, selfonly]
    gap26 = table.loc[2026, hybrid] - table.loc[2026, selfonly]

    fig, ax = g.new_figure(
        4, "Font hosting",
        "Font hosting combinations, desktop, 2022–2026",
        "Share of desktop root pages by combination of hosts; other combinations not shown",
        "pages",
        client_series=["desktop"],
    )
    g.percent_axis(ax, top=50, step=10)
    g.unit_label(ax, "percent of desktop root pages")
    x = _year_columns(ax, years)
    g.columns(ax, x, [(table[key].to_numpy(dtype=float), colour) for key, _, colour in combos],
              width=0.2, gap=0.035)
    y = g.margin_key(fig, [(label, colour) for _, label, colour in combos])
    g.margin_number(
        fig, f"{gap26:.1f}", "pts",
        f"between hybrid and self-hosted-only pages in 2026, down from {gap22:.1f} in 2022.",
        y=y + 18,
    )
    g.source_note(fig, "Source: HTTP Archive desktop root pages, mid-year crawls (2026 = July 1, 2026 "
                       "crawl). Other combinations not shown. Denominator: desktop root pages.")
    return g.save_figure(fig, 4, "hosting-combinations")


def f5():
    """F5 - WOFF2 as a share of font requests, 2019-2026."""
    df = pd.read_csv(DATA / "chart_formats.csv")
    woff2 = df[df["format"] == "woff2"].copy()
    woff2["value"] = woff2["proportion_request"].astype(float) * 100.0

    series = {
        client: part.sort_values("year")[["year", "value"]].reset_index(drop=True)
        for client, part in woff2.groupby("client")
    }
    latest = series["desktop"].set_index("year")["value"]
    _anchor("F5", "2026 desktop WOFF2 request share", latest.loc[2026], 83.7)
    unique26 = float(
        woff2[(woff2["client"] == "desktop") & (woff2["year"] == 2026)]["proportion_unique"].iloc[0]
    ) * 100.0

    fig, ax = g.new_figure(
        5, "Font formats",
        "WOFF2 share of font requests, 2019–2026",
        "Share of font requests; dots mark measured years (none for 2021 or 2023)",
        "requests",
        client_series=["desktop", "mobile"],
    )
    g.percent_axis(ax, top=100, step=20)
    g.unit_label(ax, "percent of font requests")
    # Markers mark the years actually crawled: 2021 and 2023 have no data.
    _client_lines(ax, series, label_dx=0.22, markers=True, front="desktop", where="chart_formats.csv")
    g.year_axis(ax, range(2019, 2027))
    ax.set_xlim(2018.7, 2027.6)
    g.margin_number(
        fig, f"{latest.loc[2026]:.1f}", "%",
        f"of desktop font requests were WOFF2 in July 2026, up from "
        f"{latest.loc[2019]:.1f}% in 2019.",
        note=f"Counted by distinct font URLs instead, WOFF2 is {unique26:.1f}% (Fig. 6).",
    )
    g.source_note(fig, "Source: HTTP Archive font requests, mid-year crawls (July; Aug. 2020, June 2022; "
                       "2026 = July 1, 2026 crawl). Denominator: font requests per client.")
    return g.save_figure(fig, 5, "woff2-request-share")


def f6():
    """F6 - Format mix among unique font URLs, desktop, 2024-2026."""
    # The unique-URL series starts in 2024; earlier years are never backfilled.
    years = [2024, 2025, 2026]
    order = ["woff2", "woff", "ttf", "octet-stream"]
    table = _desktop_frame(
        "chart_formats.csv",
        "format",
        value_col="proportion_unique",
        years=years,
        keys=order,
    )
    _anchor("F6", "2026 desktop WOFF2 unique-URL share", table.loc[2026, "woff2"], 68.5)

    colours = g.year_colors(years)
    names = {"woff2": "WOFF2", "woff": "WOFF", "ttf": "TTF", "octet-stream": "octet-stream"}
    print("  2026 desktop: " + ", ".join(
        f"{names[k]} {table.loc[2026, k]:.1f}%" for k in order
    ))

    fig, ax = g.new_figure(
        6, "Font formats",
        "Font formats by distinct URL, desktop, 2024–2026",
        "Share of distinct font URLs by format; other formats not shown",
        "unique_urls",
        client_series=["desktop"],
    )
    g.percent_axis(ax, top=80, step=20)
    g.unit_label(ax, "percent of distinct desktop font URLs")
    x = _category_columns(ax, [names[k] for k in order])
    g.year_groups(ax, x, [(table[order].loc[yr].to_numpy(dtype=float), colours[yr]) for yr in years],
                  width=0.22, gap=0.03, label=lambda s, i: i == 0)
    y = g.margin_key(fig, [(str(yr), colours[yr]) for yr in years])
    g.margin_number(
        fig, f"{table.loc[2026, 'woff2']:.1f}", "%",
        f"of distinct desktop font URLs were WOFF2 in 2026, up from "
        f"{table.loc[2024, 'woff2']:.1f}% in 2024.",
        y=y + 16, size_px=62,
    )
    g.source_note(fig, "Source: HTTP Archive font URLs, desktop, mid-year crawls (2026 = July 1, 2026 "
                       "crawl); series begins 2024. Denominator: distinct font URLs.")
    return g.save_figure(fig, 6, "format-mix-unique-urls")


def f7():
    """F7 - Font-related resource hints on desktop pages, 2022-2026."""
    years = [2022, 2023, 2024, 2025, 2026]
    table = _desktop_frame("chart_resource_hints.csv", "hint", years=years)

    hints = [
        ("preconnect", "preconnect", g.SERIES[0]),
        ("preload", "preload", g.SERIES[1]),
        ("dns-prefetch", "dns-prefetch", g.SERIES[2]),
    ]
    print("  2026 desktop: " + ", ".join(
        f"{label} {table.loc[2026, key]:.1f}%" for key, label, _ in hints
    ))

    fig, ax = g.new_figure(
        7, "Resource hints",
        "Font-related resource hints, desktop, 2022–2026",
        "Share of desktop root pages using each hint for a font host or font file",
        "pages",
        client_series=["desktop"],
    )
    g.percent_axis(ax, top=25, step=5)
    g.unit_label(ax, "percent of desktop root pages")
    x = _year_columns(ax, years)
    g.columns(ax, x, [(table[key].to_numpy(dtype=float), colour) for key, _, colour in hints],
              width=0.2, gap=0.035)
    y = g.margin_key(fig, [(label, colour) for _, label, colour in hints])
    g.margin_number(
        fig, f"{table.loc[2026, 'preload']:.1f}", "%",
        f"of desktop root pages preload fonts in 2026, passing dns-prefetch at "
        f"{table.loc[2026, 'dns-prefetch']:.1f}%.",
        y=y + 18,
    )
    g.source_note(fig, "Source: HTTP Archive desktop root pages, mid-year crawls (2026 = July 1, 2026 crawl). "
                       "Hints count only when they point at a font host or font file; 2022 is re-run with the "
                       f"definition used since 2024. prefetch ({table.loc[2026, 'prefetch']:.1f}% in 2026) is "
                       "not shown. Denominator: desktop root pages.")
    return g.save_figure(fig, 7, "resource-hints")


def f8():
    """F8 - font-display values on desktop pages, 2022 / 2025 / 2026."""
    # Only these three years were measured the same way; 2023-24 stay absent.
    years = [2022, 2025, 2026]
    order = ["swap", "block", "auto", "fallback", "optional"]
    table = _desktop_frame(
        "chart_font_display.csv", "property", years=years, keys=order
    )
    _anchor("F8", "2026 desktop font-display: swap", table.loc[2026, "swap"], 55.7)  # gate-corrected 2026-10-01

    colours = g.year_colors(years)
    print("  2026 desktop: " + ", ".join(
        f"{k} {table.loc[2026, k]:.1f}%" for k in order
    ))

    fig, ax = g.new_figure(
        8, "font-display",
        "font-display values, desktop, 2022, 2025 and 2026",
        "Share of desktop root pages declaring each value; pages with no value not shown; "
        "a page may declare more than one value",
        "pages",
        client_series=["desktop"],
    )
    # Grouped, never stacked: a page may declare several values, so the
    # shares overlap and do not sum to a whole.
    g.percent_axis(ax, top=60, step=10)
    g.unit_label(ax, "percent of desktop root pages")
    x = _category_columns(ax, order)
    g.year_groups(ax, x, [(table[order].loc[yr].to_numpy(dtype=float), colours[yr]) for yr in years],
                  width=0.22, gap=0.03, label=lambda s, i: i == 0)
    y = g.margin_key(fig, [(str(yr), colours[yr]) for yr in years])
    g.margin_number(
        fig, f"{table.loc[2026, 'swap']:.1f}", "%",
        f"of desktop root pages use swap, up "
        f"{table.loc[2026, 'swap'] - table.loc[2025, 'swap']:.1f} points from 2025.",
        y=y + 16, size_px=62,
    )
    g.source_note(fig, "Source: HTTP Archive desktop root pages, mid-year crawls (2026 = July 1, 2026 crawl); "
                       "only these three years were measured the same way. 2026 values are corrected for "
                       "stylesheets the extraction set aside for size. Denominator: desktop root pages.")
    return g.save_figure(fig, 8, "font-display")


def f9():
    """F9 - Font file size percentiles, 2026, log kB (per distinct parsed font file)."""
    df = pd.read_csv(SQL / "performance" / "fonts_size.csv")
    for required in ("client", "percentile", "size"):
        if required not in df.columns:
            raise ValueError(
                f"fonts_size.csv: expected {required!r}, found {list(df.columns)}"
            )
    df = df.copy()
    df["kb"] = df["size"].astype(float) / 1000.0  # source column is bytes; SI kB (2026-10-01 ruling)

    percentiles = [10, 25, 50, 75, 90, 99]
    rows = {}
    for client in ("desktop", "mobile"):
        part = df[df["client"] == client].set_index("percentile")["kb"]
        missing = [p for p in percentiles if p not in part.index]
        if missing:
            raise ValueError(f"fonts_size.csv: {client} missing p{missing}")
        rows[client] = [float(part.loc[p]) for p in percentiles]

    _anchor("F9", "2026 desktop p50", rows["desktop"][2], 35.3, tol=0.5, unit=" kB")
    _anchor("F9", "2026 desktop p99", rows["desktop"][5], 874.7, tol=5.0, unit=" kB")

    fig, ax = g.new_figure(
        9, "File sizes",
        "Font file size by percentile, 2026",
        "10th to 99th percentile, per distinct parsed font file; desktop and mobile",
        "files",
        client_series=["desktop", "mobile"],
    )
    g.unit_label(ax, "kB per file, log scale · percentiles of distinct font files")

    positions = {"desktop": 1.0, "mobile": 0.0}
    for client, values in rows.items():
        colour = g.CLIENT_COLORS[client]
        y = positions[client]
        ax.plot([values[0], values[-1]], [y, y], color=colour, alpha=0.35, lw=1.4, zorder=2)
        ax.scatter(values, [y] * len(values), s=46, color=colour, zorder=3,
                   edgecolor=g.GROUND, linewidth=1.2)
        for p, value in zip(percentiles, values):
            if client == "desktop":
                g.text(ax, value, y + 0.2, f"p{p}", color=g.MUTED, ha="center", va="bottom")
            if p in (50, 99):
                g.text(ax, value, y - 0.2, f"{value:,.1f}", color=g.INK, ha="center", va="top")
        print(f"  {client}: " + ", ".join(
            f"p{p} {v:,.1f}kB" for p, v in zip(percentiles, values)
        ))

    g.log_kb_axis(ax, ticks=(10, 100, 1000), lo=5.5, hi=1800)
    g.category_axis(ax, [0.0, 1.0], ["Mobile", "Desktop"], axis="y")
    ax.set_ylim(-0.65, 1.65)
    d = rows["desktop"]
    g.margin_number(
        fig, f"{d[5]:.1f}", "kB",
        f"is the 99th-percentile desktop font file, nearly 0.9\u00a0MB; the median is "
        f"{d[2]:.1f}\u00a0kB.",
        note=f"Three-quarters of files stay under {d[3]:.1f}\u00a0kB. "
             f"Mobile p99: {rows['mobile'][5]:.1f}\u00a0kB.",
    )
    g.source_note(fig, "Source: HTTP Archive parsed font files, July 1, 2026 crawl; SI kilobytes "
                       "(1 kB = 1,000 bytes). Denominator: distinct font files per client.")
    return g.save_figure(fig, 9, "size-percentiles")


def f10():
    """F10 - Script coverage among desktop font files, 2026."""
    df = pd.read_csv(SQL / "design" / "fonts_script.csv")
    data = df[df["client"] == "desktop"].set_index("script")["proportion"] * 100.0

    # Katakana and Hiragana are reported as separate scripts and a file may
    # cover both, so they are shown as they are measured, never summed.
    wanted = [
        ("Latin", "Latin"),
        ("PUA", "Private Use Area (mostly icons)"),
        ("Cyrillic", "Cyrillic"),
        ("Greek", "Greek"),
        ("Emoji", "Emoji-range symbols"),
        ("Katakana", "Katakana"),
        ("Hiragana", "Hiragana"),
        ("Hebrew", "Hebrew"),
        ("Devanagari", "Devanagari"),
        ("Hangul", "Hangul (near-complete sets)"),
        ("Arabic", "Arabic"),
        ("Han", "Han (near-complete sets)"),
    ]
    missing = [key for key, _ in wanted if key not in data.index]
    if missing:
        raise ValueError(f"fonts_script.csv: no desktop rows for {missing}")

    latin = _anchor("F10", "2026 desktop Latin coverage", data.loc["Latin"], 57.0, tol=0.5)
    han = _anchor("F10", "2026 desktop Han coverage", data.loc["Han"], 0.5)

    bars = sorted(
        ((label, float(data.loc[key])) for key, label in wanted),
        key=lambda item: item[1],
        reverse=True,
    )
    print("  " + ", ".join(f"{label} {value:.1f}%" for label, value in bars))

    fig, ax = g.new_figure(
        10, "Scripts",
        "Script coverage among font files, desktop, 2026",
        "Share of distinct font files covering more than 5% of each script's characters",
        "files",
        plot_l=262, plot_top=g.PLOT_TOP + 16,
        client_series=["desktop"],
    )
    g.horizontal(ax)
    g.unit_label(ax, "percent of distinct desktop font files")

    y = np.arange(len(bars))[::-1]
    for pos, (label, value) in zip(y, bars):
        # 2026-10-01: no accent; Han 0.5% is a coverage-rule artifact, not a finding
        ax.barh(pos, value, height=0.62, color=g.SERIES[0], zorder=3, linewidth=0)
        g.text(ax, value + 0.8, pos, f"{value:.1f}", color=g.MUTED, ha="left", va="center",
               bbox=dict(boxstyle="square,pad=0.12", fc=g.GROUND, ec="none"))  # knock out gridlines

    g.percent_axis(ax, top=60, step=10, axis="x")
    ax.set_xlim(0, 66)  # room for the Latin value label past the 60 tick
    g.category_axis(ax, y, [label for label, _ in bars], axis="y")
    ax.set_ylim(-0.6, len(bars) - 0.4)
    g.margin_number(
        fig, f"{latin:.0f}", "%",
        "of distinct desktop font files cover more than 5% of the Latin script.",
        note=f"Han counts only where a file carries a near-complete set (about {han:.1f}% "
             "of files); Google serves CJK fonts as many partial subsets.",
    )
    g.source_note(fig, "Source: HTTP Archive font URLs, desktop, July 1, 2026 crawl. A script counts "
                       "when a file covers more than 5% of its characters. Denominator: font files.")
    return g.save_figure(fig, 10, "script-coverage")


FIGURES = {
    "F1": f1,
    "F2": f2,
    "F4": f4,
    "F5": f5,
    "F6": f6,
    "F7": f7,
    "F8": f8,
    "F9": f9,
    "F10": f10,
}


def main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    if argv == ["--all"]:
        keys = list(FIGURES)
    else:
        keys = [a.upper() for a in argv]

    unknown = [k for k in keys if k not in FIGURES]
    if unknown:
        print(
            f"Unknown figure(s): {', '.join(unknown)}. "
            f"Known: {', '.join(FIGURES)}",
            file=sys.stderr,
        )
        return 2

    stopped = []
    for key in keys:
        print(f"{key}: rendering")
        try:
            svg, png = FIGURES[key]()
        except AnchorMismatch as exc:
            stopped.append(key)
            print(f"  STOP {exc}", file=sys.stderr)
            continue
        print(f"  -> {svg.name}, {png.name}")

    if stopped:
        print(
            f"\nNot drawn (anchor mismatch): {', '.join(stopped)}", file=sys.stderr
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
