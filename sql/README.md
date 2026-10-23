# Saved query results

Each `name.csv` is the saved result of one analysis query, grouped by topic:
`design/`, `development/`, `performance/` (the report's measurements) and
`coverage/` (what share of crawled root pages the language and country cuts cover).

**The queries themselves are not published in this repository.** The CSVs are the
record of what they produced. Where a figure in `figures/` quotes one of these
numbers, `render.py` checks the CSV against the value the report gives before
it draws (tolerance 0.2 percentage points).

The queries ran on the public `httparchive.crawl.*` BigQuery tables (2026-07-01
crawl), mostly against compact materialized intermediate tables
(`fonts_2026.pruned_css`, `font_requests`, `root_pages`) built once from the crawl
to keep the suite affordable; `../expenses/` itemizes every job billed. The
Python runners kept here (`execute*.py`, `estimate_full.py`, `validate_*.py`)
are the machinery that executed, dry-run-estimated, and spot-checked the suite —
they contain no query text.
