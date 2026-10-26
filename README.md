# Fonts on the Web in 2026 - Analysis

The report, results and figures behind "Fonts on the Web in 2026," using data from the HTTP Archive crawl to understand how fonts are hosted, packaged, loaded and designed across the web. It reads the crawl of 1 July 2026 (11.6 million desktop and 15.5 million mobile root pages) and compares it with the Web Almanac Fonts chapters of 2019, 2020, 2022, 2024 and 2025; the Almanac is not publishing in 2026, so this report carries that series forward as a standalone study. It was commissioned by Google Fonts and written by Charles Berret.

## What is here

| Directory | Contents |
| --- | --- |
| `report/` | The report: `fonts-on-the-web-2026.md` (Markdown, with its 58 footnotes and the figures linked from `figures/out/`) and `fonts-on-the-web-2026.pdf` (37 pages). Draft v10, 23 October 2026. |
| `figures/` | `render.py` draws the nine figures from the CSVs; `grammar.py` is the one style file; renders are in `out/` as PNG (1600 px wide) and SVG. `README.md` describes the frame, the palette and the type. |
| `sql/` | The saved result of every analysis query (`name.csv`), grouped by section: `design/`, `development/`, `performance/`, and `coverage/` for the page-language and country cuts. The runners that executed and cost-checked the suite are kept; the query text is not published (see `sql/README.md`). |
| `data/` | `multi-year/`: chart-ready CSVs spanning 2011 to 2026, with provenance and caveats in its README (including which years are request shares and which are distinct-URL shares). At the top level, a Google Fonts catalogue snapshot and the script that reproduces the catalogue-share figures. |
| `verification/` | How the numbers were checked: the claim-by-claim sheet, the source maps that tie each number in the text to a result file, the gate script that re-checks a draft against them, and its report on the published text. `README.md` there explains how to read them. |
| `expenses/` | What the analysis cost to run: every BigQuery job itemized, daily totals and a summary. |

## Reading the report

Start with `report/fonts-on-the-web-2026.md` or the PDF. The Introduction states the three findings; each section names the denominator its percentages use (pages, requests, distinct font URLs or parsed font files), because the same fact reads differently on each. Appendix B sets out the method and its limits, including the caveats that matter most: the 2023 enlargement of the crawl, the CSS figures that are floors, and the unexplained steps in Google's mobile series.

## Reproducing the figures

No BigQuery access is needed; the CSVs are included.

```bash
cd figures
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.lock.txt
./.venv/bin/python render.py --all
```

Fonts for the figures are fetched from Google Fonts on first run. Every figure names its denominator. A figure whose headline number is quoted in the report checks the CSV against that number before it draws, and stops if they disagree by more than 0.2 percentage points. Years that were not measured are left out, never interpolated.

## Checking the numbers

```bash
python3 verification/verify_draft_numbers.py --draft report/fonts-on-the-web-2026.md --date YYYY-MM-DD
```

The gate reads the two source maps, checks that every mapped value appears in the text and that every number in the text traces to a map row or a data cell, and writes `verification/report-<date>.md`. The report shipped with this repository is the run on the published text.

## Cost

`expenses/` itemizes every BigQuery job the pipeline ran, so the cost of reproducing the analysis is visible before anyone starts: 549 jobs, 88.5 TiB billed, about $553 at list price. `sql/estimate_full.py` is the estimator that was used to check query cost before any run.

## Citation

`CITATION.cff` gives a citation. The crawl data come from the HTTP Archive; cite it alongside this repository.
