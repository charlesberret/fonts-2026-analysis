# Convenor evidence — Google mobile anomaly (checked 2026-09-03, during round)

Query against `fonts_all_years.duckdb` → `y2025_performance_which_services_are`
(the 2025 chapter's own sheet mirror), Google page share:

| Crawl | Desktop | Mobile |
|-------|--------:|-------:|
| 2022-07-01 | 59.8% | 51.5% |
| 2023-07-01 | 55.6% | 46.3% |
| 2024-07-01 | 56.8% | 47.5% |
| 2025-07-01 | 53.7% | 47.2% |
| 2026-07-01 (new) | 53.7% | **51.9%** |

Conclusion: 2025's "47%" is **not** a transcription outlier — mobile held at
46–47.5% for three consecutive crawls under the same SERVICE() methodology.
2026's 51.9% is a real +4.7pt discontinuity, back to the 2022 level, while
desktop is exactly flat. Plan implication: workstream A investigates the 2026
mobile side (crawl composition, mobile page universe size, SERVICE() edge
cases on the 2026 materialize), and the prose keeps the careful-sentence
treatment if unexplained. Do not publish "continued mobile decline."
