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
    g.end_labels(ax, ends, dx=label_dx, colors=[g.CLIENT_COLORS["desktop"], g.CLIENT_COLORS["mobile"]])
    return latest


def f1():
    """Figure 1 - Pages requesting at least one web font, 2011-2026."""
    series = _annual_series("chart_font_usage_annual.csv")
    fig, ax = g.new_figure(
        1, "Adoption",
        "Pages Using Web Fonts, 2011–2026",
        "What share of root pages request at least one web font? Desktop and mobile are counted separately.",
        "pages",
        client_series=["desktop", "mobile"],
    )
    g.percent_axis(ax, top=100, step=20)
    g.unit_label(ax, "percent of pages")
    latest = _client_lines(ax, series, label_dx=0.55, front="desktop", where="chart_font_usage_annual.csv")
    years = list(series["desktop"]["year"])
    g.year_axis(ax, years, step=3)
    ax.set_xlim(2010.4, 2029.6)
    g.grid_to(ax, 2026)
    first = float(series["desktop"].iloc[0]["value"])
    gain = latest["desktop"] - float(series["desktop"].set_index("year")["value"].loc[2025])
    if not 0 <= gain < 1:  # the callout says "by only"; the prose says "less than a point"
        raise AnchorMismatch(f"Figure 1: desktop gain since 2025 is {gain:.2f} pts, not under 1.")
    if not 87.5 <= latest["desktop"] < 90:  # the callout says "nearly nine in ten"
        raise AnchorMismatch(f"Figure 1: desktop share {latest['desktop']:.1f}% no longer reads as nearly nine in ten.")
    g.margin_number(
        fig, f"{latest['desktop']:.1f}", "%",
        f"Nearly nine in ten desktop web pages use a web font. Mobile is {latest['mobile']:.1f}%.",
        note=f"The curve has flattened: up {gain:.1f} points since last year, following a steep rise from {first:.1f}% in 2011.",
    )
    g.source_note(fig, "Source: HTTP Archive root pages, July crawls (July 1 or July 15 each year; "
                       "2026 = July 1, 2026 crawl). Percentages are of all root pages counted for each device.")
    return g.save_figure(fig, 1, "font-usage-over-time")


def f9():
    """Figure 9 - Pages using at least one variable font, 2019-2026."""
    series = _annual_series("chart_variable_fonts.csv")
    fig, ax = g.new_figure(
        9, "Variable Fonts",
        "Pages Using Variable Fonts, 2019–2026",
        "What share of root pages load at least one variable font, whether or not the author chose it. "
        "Desktop and mobile are counted separately.",
        "pages",
        client_series=["desktop", "mobile"],
    )
    g.percent_axis(ax, top=60, step=10)
    g.unit_label(ax, "percent of pages")
    latest = _client_lines(ax, series, label_dx=0.22, where="chart_variable_fonts.csv")
    g.year_axis(ax, range(2019, 2027))
    ax.set_xlim(2018.7, 2027.9)
    g.grid_to(ax, 2026)
    for client in ("desktop", "mobile"):  # the note says both gained about nine points, the biggest since 2022
        yoy = series[client].set_index("year")["value"].diff()
        if not (abs(yoy.loc[2026] - 9) <= 0.5 and yoy.loc[2026] > yoy.loc[2023:2025].max()):
            raise AnchorMismatch(f"Figure 9: {client} gain {yoy.loc[2026]:.1f} pts no longer 'about nine, biggest since 2022'.")
    g.margin_number(
        fig, f"{latest['mobile']:.1f}", "%",
        f"Half of mobile pages now load a variable font. Desktop is {latest['desktop']:.1f}%.",
        note="Both gained about nine points in a year, the biggest rise since 2022.",
    )
    g.source_note(fig, "Source: HTTP Archive root pages, mid-year crawls (July; Sept. 2020, June 2022; "
                       "2021 via the 2022 chapter). Percentages are of all root pages counted for each device.")
    return g.save_figure(fig, 9, "variable-font-adoption")


# --------------------------------------------------------------------------
# Column helpers (shared by Figures 2, 4, 6 and 7)
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


def f2():
    """Figure 2 - How desktop pages combine Google Fonts and self-hosting, 2022-2026."""
    years = [2022, 2023, 2024, 2025, 2026]
    table = _desktop_frame("chart_service_combos.csv", "services", years=years)

    combos = [
        ("Google, self-hosted", "Both Google and self-hosted", g.VIOLET),
        ("self-hosted", "Self-hosted only", g.CERISE),
        ("Google", "Google only", g.COBALT),
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
    _anchor("Figure 2", "2026 desktop hybrid share", table.loc[2026, hybrid], 35.2)
    _anchor("Figure 2", "2026 desktop self-hosted-only share", table.loc[2026, selfonly], 32.2)
    # The callout is the two Google rows summed, a number the bars do not show.
    google_total = table.loc[2026, hybrid] + table.loc[2026, "Google"]
    _anchor("Figure 2", "2026 desktop Google-only plus hybrid", google_total, 49.5)
    # Google's full reach, which adds pages that mix it with a third host (chart_services.csv).
    services = pd.read_csv(DATA / "chart_services.csv")
    google_reach = float(services[(services["year"] == 2026) & (services["client"] == "desktop")
                                  & (services["service"] == "Google")]["proportion"].iloc[0]) * 100.0
    _anchor("Figure 2", "2026 desktop Google Fonts reach", google_reach, 53.7)

    fig, ax = g.new_figure(
        2, "Font Hosting",
        "Font Hosting Combinations, 2022–2026",
        "How do desktop pages get their fonts: from Google, from their own servers, or both? Other combinations are not shown.",
        "pages",
        client_series=["desktop"],
    )
    g.percent_axis(ax, top=50, step=10)
    g.unit_label(ax, "percent of desktop pages")
    x = _year_columns(ax, years)
    g.columns(ax, x, [(table[key].to_numpy(dtype=float), colour) for key, _, colour in combos],
              width=0.2, gap=0.035)
    y = g.margin_key(fig, [(label, colour) for _, label, colour in combos])
    g.margin_number(
        fig, f"{google_total:.1f}", "%",
        "of desktop pages use Google Fonts, alone or with self-hosting.",
        note=f"Adding pages that mix Google with a third host, its reach is {google_reach:.1f}%.",
        y=y + 18,
    )
    g.source_note(fig, "Source: HTTP Archive desktop root pages, mid-year crawls (2026 = July 1, 2026 "
                       "crawl). Other combinations not shown. Percentages are of all desktop root pages.")
    return g.save_figure(fig, 2, "hosting-combinations")


def f3():
    """Figure 3 - WOFF2 as a share of font requests, 2019-2026."""
    df = pd.read_csv(DATA / "chart_formats.csv")
    woff2 = df[df["format"] == "woff2"].copy()
    woff2["value"] = woff2["proportion_request"].astype(float) * 100.0

    series = {
        client: part.sort_values("year")[["year", "value"]].reset_index(drop=True)
        for client, part in woff2.groupby("client")
    }
    latest = series["desktop"].set_index("year")["value"]
    _anchor("Figure 3", "2026 desktop WOFF2 request share", latest.loc[2026], 83.7)
    unique26 = float(
        woff2[(woff2["client"] == "desktop") & (woff2["year"] == 2026)]["proportion_unique"].iloc[0]
    ) * 100.0

    fig, ax = g.new_figure(
        3, "Font Formats",
        "WOFF2 Share of Font Requests, 2019–2026",
        "What share of font requests use WOFF2, the modern compressed format? Dots mark the years we counted. There is no data for 2021 or 2023.",
        "requests",
        client_series=["desktop", "mobile"],
    )
    g.percent_axis(ax, top=100, step=20)
    g.unit_label(ax, "percent of font requests")
    # Markers mark the years actually crawled: 2021 and 2023 have no data.
    _client_lines(ax, series, label_dx=0.22, markers=True, front="desktop", where="chart_formats.csv")
    g.year_axis(ax, range(2019, 2027))
    ax.set_xlim(2018.7, 2027.9)
    g.grid_to(ax, 2026)
    g.margin_number(
        fig, f"{latest.loc[2026]:.1f}", "%",
        f"Over four in five desktop font requests are for WOFF2, up from "
        f"{latest.loc[2019]:.1f}% in 2019.",
        note=f"Counting each distinct font file once, WOFF2 is {unique26:.1f}% (Figure 4). "
             "Popular hosts serve it so often that the request share runs higher.",
    )
    g.source_note(fig, "Source: HTTP Archive font requests, mid-year crawls (July; Aug. 2020, June 2022; "
                       "2026 = July 1, 2026 crawl). Percentages are of all font requests per device.")
    return g.save_figure(fig, 3, "woff2-request-share")


def f4():
    """Figure 4 - Format mix among unique font URLs, desktop, 2024-2026."""
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
    _anchor("Figure 4", "2026 desktop WOFF2 unique-URL share", table.loc[2026, "woff2"], 68.5)

    colours = g.year_colors(years)
    names = {"woff2": "WOFF2", "woff": "WOFF", "ttf": "TTF", "octet-stream": "Unidentified (octet-stream)"}
    print("  2026 desktop: " + ", ".join(
        f"{names[k]} {table.loc[2026, k]:.1f}%" for k in order
    ))

    fig, ax = g.new_figure(
        4, "Font Formats",
        "Font Formats by Distinct URL, 2024–2026",
        "What share of distinct desktop font files use each format? Other formats are not shown.",
        "unique_urls",
        client_series=["desktop"],
    )
    g.percent_axis(ax, top=80, step=20)
    g.unit_label(ax, "percent of distinct desktop font URLs")
    x = _category_columns(ax, [names[k] for k in order])
    g.year_groups(ax, x, [(table[order].loc[yr].to_numpy(dtype=float), colours[yr]) for yr in years],
                  width=0.22, gap=0.03, label=lambda s, i: i == 0)
    y = g.margin_key(fig, [(str(yr), colours[yr]) for yr in years])
    if not (table.loc[2026, "woff2"] > 200 / 3 and abs(table.loc[2026, "ttf"] - table.loc[2024, "ttf"]) < 1):
        raise AnchorMismatch("Figure 4: WOFF2 no longer over two-thirds, or TTF no longer barely moved.")
    g.margin_number(
        fig, f"{table.loc[2026, 'woff2']:.1f}", "%",
        f"Over two-thirds of distinct font files are WOFF2, up from "
        f"{table.loc[2024, 'woff2']:.1f}% in 2024.",
        note=f"WOFF fell from {table.loc[2024, 'woff']:.1f}% to {table.loc[2026, 'woff']:.1f}% "
             f"as WOFF2 rose. TTF barely moved, from {table.loc[2024, 'ttf']:.1f}% to "
             f"{table.loc[2026, 'ttf']:.1f}%.",
        y=y + 16,
    )
    g.source_note(fig, "Source: HTTP Archive font URLs, desktop, mid-year crawls (2026 = July 1, 2026 "
                       "crawl); series begins 2024. Percentages are of distinct font URLs.")
    return g.save_figure(fig, 4, "format-mix-unique-urls")


def f6():
    """Figure 6 - Font-related resource hints on desktop pages, 2022-2026."""
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
        6, "Resource Hints",
        "Font Resource Hints, 2022–2026",
        "What share of desktop pages ask the browser to prepare early for fonts? "
        "Hints from authors and from tools look alike.",
        "pages",
        client_series=["desktop"],
    )
    g.percent_axis(ax, top=25, step=5)
    g.unit_label(ax, "percent of desktop pages")
    x = _year_columns(ax, years)
    g.columns(ax, x, [(table[key].to_numpy(dtype=float), colour) for key, _, colour in hints],
              width=0.2, gap=0.035)
    y = g.margin_key(fig, [(label, colour) for _, label, colour in hints])
    t = table
    ok = (1.7 <= t.loc[2026, "preconnect"] / t.loc[2022, "preconnect"] < 2.0           # "nearly doubled"
          and t.loc[2026, "preconnect"] > max(t.loc[2026, "preload"], t.loc[2026, "dns-prefetch"])  # "leads"
          and t.loc[2026, "preload"] > t.loc[2026, "dns-prefetch"]                       # "passed ... this year"
          and t.loc[2025, "preload"] < t.loc[2025, "dns-prefetch"])
    if not ok:
        raise AnchorMismatch("Figure 6: the hint ranking no longer matches the callout.")
    g.margin_number(
        fig, f"{t.loc[2026, 'preconnect']:.1f}", "%",
        "Preconnect has nearly doubled since 2022 and leads every other font hint.",
        note=f"Preload passed dns-prefetch this year, {t.loc[2026, 'preload']:.1f}% to "
             f"{t.loc[2026, 'dns-prefetch']:.1f}%. dns-prefetch was "
             f"{t.loc[2022, 'dns-prefetch']:.1f}% in 2022.",
        y=y + 18,
    )
    g.source_note(fig, "Source: HTTP Archive desktop root pages, mid-year crawls (2026 = July 1, 2026 crawl). "
                       "Hints count only when they point at a font host or font file; 2022 is re-run with the "
                       f"definition used since 2024. prefetch ({table.loc[2026, 'prefetch']:.1f}% in 2026) is "
                       "not shown. Percentages are of all desktop root pages.")
    return g.save_figure(fig, 6, "resource-hints")


def f7():
    """Figure 7 - font-display values on desktop pages, 2022 / 2025 / 2026."""
    # Only these three years were measured the same way; 2023-24 stay absent.
    years = [2022, 2025, 2026]
    order = ["swap", "block", "auto", "fallback", "optional"]
    table = _desktop_frame(
        "chart_font_display.csv", "property", years=years, keys=order
    )
    _anchor("Figure 7", "2026 desktop font-display: swap", table.loc[2026, "swap"], 55.7)  # gate-corrected 2026-10-01

    colours = g.year_colors(years)
    print("  2026 desktop: " + ", ".join(
        f"{k} {table.loc[2026, k]:.1f}%" for k in order
    ))

    fig, ax = g.new_figure(
        7, "font-display",
        "font-display Values, 2022, 2025 and 2026",
        "What share of desktop pages set each value for how text looks while a font loads? "
        "A page may set several.",
        "pages",
        client_series=["desktop"],
    )
    # Grouped, never stacked: a page may declare several values, so the
    # shares overlap and do not sum to a whole.
    g.percent_axis(ax, top=60, step=10)
    g.unit_label(ax, "percent of desktop pages")
    x = _category_columns(ax, order)
    g.year_groups(ax, x, [(table[order].loc[yr].to_numpy(dtype=float), colours[yr]) for yr in years],
                  width=0.22, gap=0.03, label=lambda s, i: i == 0)
    y = g.margin_key(fig, [(str(yr), colours[yr]) for yr in years])
    g.margin_number(
        fig, f"{table.loc[2026, 'swap']:.1f}", "%",
        f"Swap is now on over half of desktop pages, up "
        f"{table.loc[2026, 'swap'] - table.loc[2025, 'swap']:.1f} points from last year.",
        note=f"block holds at {table.loc[2026, 'block']:.1f}%, largely an icon-font default "
             "rather than a choice for body text.",
        y=y + 16,
    )
    g.source_note(fig, "Source: HTTP Archive desktop root pages, mid-year crawls (2026 = July 1, 2026 crawl); "
                       "only these three years were measured the same way. 2026 values are corrected for "
                       "stylesheets the extraction set aside for size. Pages that set no value are not shown. "
                       "Percentages are of all desktop root pages.")
    return g.save_figure(fig, 7, "font-display")


def f5():
    """Figure 5 - Font file size percentiles, 2026, log kB (per distinct parsed font file)."""
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

    _anchor("Figure 5", "2026 desktop p50", rows["desktop"][2], 35.3, tol=0.5, unit=" kB")
    _anchor("Figure 5", "2026 desktop p99", rows["desktop"][5], 874.7, tol=5.0, unit=" kB")

    fig, ax = g.new_figure(
        5, "File Sizes",
        "Font File Size by Percentile, 2026",
        "How big are font files? Each dot is a percentile: p50 is the middle file, and p99 is bigger than 99 of every 100. "
        "Each distinct font file counts once.",
        "files",
        client_series=["desktop", "mobile"],
    )
    g.unit_label(ax, "kilobytes (kB) per file, on a log scale, for distinct font files")

    positions = {"desktop": 1.0, "mobile": 0.0}
    for client, values in rows.items():
        colour = g.CLIENT_COLORS[client]
        y = positions[client]
        ax.plot([values[0], values[-1]], [y, y], color=colour, alpha=0.35, lw=1.4, zorder=2)
        ax.scatter(values, [y] * len(values), s=46, color=colour, zorder=3,
                   edgecolor=g.GROUND, linewidth=1.2)
        # the median is what the callout cites: a larger dot with a ground-coloured centre
        ax.scatter([values[2]], [y], s=82, color=colour, zorder=4, edgecolor=g.GROUND, linewidth=1.2)
        ax.scatter([values[2]], [y], s=12, color=g.GROUND, zorder=5, linewidth=0)
        for p, value in zip(percentiles, values):
            if client == "desktop":
                g.text(ax, value, y + 0.2, f"p{p}", color=g.MUTED, ha="center", va="bottom")
            if p in (50, 99):
                g.text(ax, value, y - 0.2, f"{value:,.1f}", color=g.INK, ha="center", va="top",
                       bbox=dict(boxstyle="square,pad=0.3", fc=g.GROUND, ec="none"))
        print(f"  {client}: " + ", ".join(
            f"p{p} {v:,.1f}kB" for p, v in zip(percentiles, values)
        ))

    g.log_kb_axis(ax, ticks=(10, 100, 1000), lo=5.5, hi=1800, grid_color="#cfd1d9")
    g.category_axis(ax, [0.0, 1.0], ["Mobile", "Desktop"], axis="y")
    ax.set_ylim(-0.65, 1.65)
    d = rows["desktop"]
    g.margin_number(
        fig, f"{d[5]:.1f}", "kB",
        f"The heaviest 1% of desktop font files start there. The median is "
        f"{d[2]:.1f}\u00a0kB.",
        note=f"Three-quarters of files stay under {d[3]:.1f}\u00a0kB. Adobe-served OpenType "
             "files alone make up more than a quarter of the heaviest 1%.",
    )
    g.source_note(fig, "Source: HTTP Archive parsed font files, July 1, 2026 crawl; SI kilobytes "
                       "(1 kB = 1,000 bytes). Percentages are of distinct font files per device.")
    return g.save_figure(fig, 5, "size-percentiles")


def f8():
    """Figure 8 - Script coverage among desktop font files, 2026."""
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
        ("Hangul", "Hangul"),
        ("Arabic", "Arabic"),
        ("Han", "Han (Chinese characters), 4,920 and up"),
    ]
    missing = [key for key, _ in wanted if key not in data.index]
    if missing:
        raise ValueError(f"fonts_script.csv: no desktop rows for {missing}")

    latin = _anchor("Figure 8", "2026 desktop Latin coverage", data.loc["Latin"], 57.0, tol=0.5)
    han = _anchor("Figure 8", "2026 desktop Han coverage", data.loc["Han"], 0.5)

    bars = sorted(
        ((label, float(data.loc[key])) for key, label in wanted),
        key=lambda item: item[1],
        reverse=True,
    )
    print("  " + ", ".join(f"{label} {value:.1f}%" for label, value in bars))

    fig, ax = g.new_figure(
        8, "Scripts",
        "Script Coverage of Font Files, 2026",
        "What share of distinct desktop font files cover a substantial part of each script, or writing system?",
        "files",
        plot_l=286, plot_top=g.PLOT_TOP + 16,
        client_series=["desktop"],
    )
    g.horizontal(ax)
    g.unit_label(ax, "percent of distinct desktop font files")

    y = np.arange(len(bars))[::-1]
    for pos, (label, value) in zip(y, bars):
        # 2026-10-01: no accent; Han 0.5% is a coverage-rule artifact, not a finding
        ax.barh(pos, value, height=0.62, color=g.SERIES[0], zorder=3, linewidth=0)
        han_row = label.startswith("Han (")   # the callout is about this row
        g.text(ax, value + 0.8, pos, f"{value:.1f}", color=g.INK if han_row else g.MUTED,
               weight=500 if han_row else "normal", ha="left", va="center",
               bbox=dict(boxstyle="square,pad=0.12", fc=g.GROUND, ec="none"))  # knock out gridlines

    g.percent_axis(ax, top=60, step=10, axis="x")
    ax.set_xlim(0, 66)  # room for the Latin value label past the 60 tick
    g.category_axis(ax, y, [label for label, _ in bars], axis="y")
    ax.set_ylim(-0.6, len(bars) - 0.4)
    g.margin_number(
        fig, f"{han:.1f}", "%",
        "of font files cover a substantial set of Han characters. Most pages receive Han in slices of a "
        "few hundred characters.",
        note="One page using Noto Sans JP fetches about 27.",
    )
    g.source_note(fig, "Source: HTTP Archive font URLs, desktop, July 1, 2026 crawl. A script counts "
                       "when a file covers more than 5% of its characters. Percentages are of all font files.")
    return g.save_figure(fig, 8, "script-coverage")


# Figures are numbered in the order they appear in the draft (renumbered 2026-10-17).
# Old numbers: 1->1, 4->2, 5->3, 6->4, 9->5, 7->6, 8->7, 10->8, 2->9. Old PNG/SVG names are stale.
FIGURES = {
    "F1": f1,
    "F2": f2,
    "F3": f3,
    "F4": f4,
    "F5": f5,
    "F6": f6,
    "F7": f7,
    "F8": f8,
    "F9": f9,
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
        print(f"Figure {key[1:]}: rendering")
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
