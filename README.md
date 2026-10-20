# fonts-2026-analysis

Queries, results and figures behind the 2026 Fonts chapter of the
[HTTP Archive Web Almanac](https://almanac.httparchive.org/): how fonts are hosted, packaged,
loaded and designed across the web, from the 2026-07-01 crawl, compared with earlier years.

| Directory | Contents |
| --- | --- |
| `sql/` | The BigQuery queries and the saved result of each (`name.sql` beside `name.csv`), grouped by topic: `design/`, `development/`, `performance/`, plus `materialize/` for the pruned working tables. `execute*.py` run them. |
| `data/` | Chart-ready CSVs spanning 2011-2026 in `multi-year/` (`chart_*.csv`; its `README.md` gives provenance and methodology caveats, including which years use request share and which use unique-URL share). At top level: a Google Fonts catalogue snapshot (2026-10-12) and per-service font-family totals for self-hosted vs Google. |
| `figures/` | `render.py` draws nine figures (F1–F9) from the CSVs. Output lands in `figures/out/` as SVG and PNG. |

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

## Re-run the queries

The queries run against the public `httparchive` datasets in BigQuery and write to a dataset in a
project you own. Change the `PROJECT_ID` constant (and `DATASET_ID`, where a script sets one) at the top of each
`sql/*.py` script you run, authenticate with `gcloud auth application-default login`, and
install `sql/requirements.txt`. Scanning the full crawl costs real money; `sql/estimate_full.py`
prints the estimated bytes first.

## Licence

Code: MIT (`LICENSE`). Data and figures: CC BY 4.0 (`LICENSE-DATA.md`).
