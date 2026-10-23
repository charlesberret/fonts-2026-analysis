# Multi-year chart data (Fonts)

Built **2026-08-04** from local Sheet exports in `fonts_all_years.duckdb` (repo root, `web-almanac/fonts_all_years.duckdb`; 2019–2025 Almanac spreadsheets) plus **2026-07-01** pipeline CSVs under `fonts-2026/sql/`.

## Chart-ready files (use these first)

| File | Grain | Notes |
|------|-------|-------|
| `chart_font_usage_annual.csv` | year × client | Pages requesting ≥1 font; July crawl when available; **2011–2026** |
| `chart_variable_fonts.csv` | year × client | Pages with ≥1 variable font; **2019–2026** |
| `chart_services.csv` | year × client × service | self-hosted / Google / Adobe / fontawesome.com page share; **2022–2026** |
| `chart_service_combos.csv` | year × client × combo | exclusive self, Google only, Google+self; **2022–2026** |
| `chart_resource_hints.csv` | year × client × hint | preconnect / preload / dns-prefetch / prefetch; **2022–2026** |
| `chart_font_display.csv` | year × client × property | swap / block / …; **2022, 2025, 2026** |
| `chart_formats.csv` | year × client × format | request share always; **unique-URL share from 2024+** |

## Source / intermediate extracts

`01_*.csv` … `07_*.csv` — wider dumps from DuckDB tables (headers messy where Sheets had title rows; chart_* files are cleaned).

## Rebuild

```bash
# These CSVs were exported from a DuckDB mirror of the earlier years' Web Almanac result
# spreadsheets (links below) joined to the 2026 result CSVs under ../../sql/.
# The export queries are not published; the CSVs are the record of what they produced.
duckdb fonts_all_years.duckdb   # then COPY queries in session history
```

## Methodology caveats

1. **Adoption** uses the 2025 “font usage over time” sheet (HA monthly/biweekly history) + 2026 materialize. Prefer **July** rows for annual charts.
2. **Formats 2019–2022** are mostly **request-volume** MIME shares. **Unique-URL** (`proportion_unique`) exists reliably from **2024**. Chapter prose YoY for WOFF2 should use unique-URL for 2024→2026; label request series separately.
3. **Service names** normalized: `Google` not `Google Fonts` in 2025–2026 SERVICE() output.
4. **2026** = crawl `2026-07-01` root pages only.
5. DuckDB is a **local mirror of Google Sheets exports**, not a live Sheets API pull. Refresh by re-importing XLSX into `fonts_all_years.duckdb` if Sheets change.

## Sheet IDs (upstream)

| Year | Spreadsheet |
|------|-------------|
| 2019 | `108g6LXdC3YVsxmX1CCwrmpZ3-DmbB8G_wwgQHX5pn6Q` |
| 2020 | `1jjvZqYay5KmTle4atzFWqtbkz9ohw25KFmNtCS-7n3s` |
| 2022 | `1A1XwuGa1DkqNLaF-lSXz4ndxO9G6SfACHwUvvywHgbQ` |
| 2024 | `1EkdvJ8e0B9Rr42evC2Ds5Ekwq6gF9oLBW0BA5cmSUT4` |
| 2025 | `1otdu4p_CCI70B4FVzw6k02frStsPMrQoFu7jUim_0Bg` |
