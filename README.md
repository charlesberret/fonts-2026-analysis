# Fonts on the Web in 2026 - Analysis

Queries, results and figures behind the report "Fonts on the Web in 2026," using data from the HTTP Archive crawl to understand how fonts are hosted, packaged, loaded and designed across the web.

| Directory | Contents |
| --- | --- |
| `sql/` | The saved result of each analysis query (`name.csv`), grouped by topic: `design/`, `development/`, `performance/`, `coverage/` (page language and country coverage). The queries themselves are not published; `execute*.py`, `estimate_full.py` and `validate_*.py` are the machinery that ran and checked them. |
| `data/` | Chart-ready CSVs spanning 2011-2026 in `multi-year/` (`chart_*.csv`; its `README.md` gives provenance and methodology caveats, including which years use request share and which use unique-URL share). At top level: a Google Fonts catalogue snapshot (2026-10-12) and the top-100-per-service subset of `sql/performance/fonts_family_by_service_totals.csv`; `data/catalogue_share.py` reproduces the catalogue-share figures quoted in the chapter from those two files. |
| `figures/` | `render.py` draws nine figures (F1–F9) from the CSVs. Output lands in `figures/out/` as SVG and PNG. |
| `expenses/` | What the pipeline cost: every BigQuery job itemized (`bigquery-jobs-itemized.csv`), daily totals, and `expenses-summary.md`. |

## Reproduce the figures

No BigQuery access is needed, since the CSVs are included.

```bash
cd figures
python3 -m venv .venv && ./.venv/bin/pip install -r requirements.lock.txt
./.venv/bin/python render.py --all
```

Every figure names its denominator (pages, requests, unique URLs or files). A figure whose number
is quoted in the chapter checks the CSV against that number before it draws, and stops if they
disagree by more than 0.2 percentage points. Years that were not measured are left out, never
interpolated.

## Cost

`expenses/` itemizes every BigQuery job the pipeline ran — 547 jobs, 86.1 TiB billed,
about $538 at list price — so the cost of reproducing this analysis is visible up front.
`sql/estimate_full.py` is the estimator that was used to check query cost before any run.

## Licence

Code: MIT (`LICENSE`). Data and figures: CC BY 4.0 (`LICENSE-DATA.md`).
