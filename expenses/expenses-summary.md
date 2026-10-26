# Fonts on the Web 2026: Google Cloud expenses

Prepared 2026-10-26 from BigQuery job history for project `fonts-data-analysis` (all jobs on the project, 2026-06-29 to 2026-10-26). Times are UTC.

**This is a usage statement, not the invoice.** The authoritative amounts are in the Google Cloud Billing report for the billing account. Credits, taxes and any other projects on the same account are not visible here.

## Summary

| Item | Amount |
|---|---|
| BigQuery on-demand queries: 549 jobs, 97,257,011,544,064 bytes billed (88.455 TiB) at the $6.25 per TiB list price | $552.84 |
| Same, net of the free first 1 TiB per month, if this project is the only usage on the account | $527.64 |
| BigQuery storage in dataset `fonts_2026`, accrued 2026-08-03 to 2026-10-26 at the active logical rate, no free-tier offset (estimate) | $156.85 |
| Estimated gross total, list price queries plus storage | $709.70 |
| Estimated total net of the monthly free query tier | $684.49 |

Not charged: the HTTP Archive and Chrome UX Report datasets are public. Load and extract jobs, and queries that processed no data, cost nothing. The helper bucket `gs://fonts-data-analysis-lib` holds 60 KiB.

## Rates used

- Queries: $6.25 per TiB billed, first 1 TiB per month per account free. Source: https://cloud.google.com/bigquery/pricing, read 2026-10-21.
- Storage, US multi-region, active logical: $0.000031507 per GiB-hour, first 10 GiB per month free. Same source. Tables become cheaper long-term storage after 90 days without changes.
- The project's earlier planning notes used $5 per TB; that figure is lower than the list price and is not used here.

## By month (queries)

| Month | Jobs | TiB billed | List price | After free 1 TiB |
|---|---|---|---|---|
| 2026-06 | 6 | 0.032 | $0.20 | $0.00 |
| 2026-07 | 454 | 1.405 | $8.78 | $2.53 |
| 2026-08 | 69 | 63.551 | $397.19 | $390.94 |
| 2026-09 | 6 | 2.882 | $18.01 | $11.76 |
| 2026-10 | 14 | 20.584 | $128.65 | $122.40 |

## By day, all 17 days with spend

| Date (UTC) | Jobs | TiB billed | List price |
|---|---|---|---|
| 2026-06-29 | 6 | 0.0325 | $0.20 |
| 2026-07-05 | 114 | 0.3858 | $2.41 |
| 2026-07-06 | 3 | 0.0131 | $0.08 |
| 2026-07-26 | 176 | 0.4003 | $2.50 |
| 2026-07-27 | 161 | 0.6058 | $3.79 |
| 2026-08-03 | 33 | 14.7476 | $92.17 |
| 2026-08-04 | 34 | 48.8014 | $305.01 |
| 2026-08-17 | 2 | 0.0020 | $0.01 |
| 2026-09-03 | 1 | 1.2476 | $7.80 |
| 2026-09-30 | 5 | 1.6346 | $10.22 |
| 2026-10-01 | 2 | 17.1707 | $107.32 |
| 2026-10-11 | 1 | 0.0206 | $0.13 |
| 2026-10-12 | 5 | 0.1783 | $1.11 |
| 2026-10-17 | 1 | 0.0007 | $0.00 |
| 2026-10-21 | 3 | 0.9050 | $5.66 |
| 2026-10-24 | 1 | 1.2182 | $7.61 |
| 2026-10-25 | 1 | 1.0906 | $6.82 |

## What the large days were

| Date and time (UTC) | Job | TiB | List price | What it did |
|---|---|---|---|---|
| 2026-10-01 15:00:30 | `d29efe46-71c0-446a-adbf-01ff3ce7d84e` | 17.075872 | $106.72 | SELECT: How much does the pruned_css size gate undercount each 2026 CSS page share? |
| 2026-08-04 02:21:49 | `bqjob_r4e8abc4c685f08dc_0000019fca93c248_1` | 15.793375 | $98.71 | CREATE_TABLE_AS_SELECT: Materialize July 2026 font-relevant CSS once. |
| 2026-09-03 19:43:57 | `41f13b78-4025-4df5-b433-c8078e2f36aa` | 1.247569 | $7.80 | SELECT: Where does unicode-range subsetting come from — Google Fonts' generated CSS, first-party C |
| 2026-09-30 20:59:27 | `b550416f-b57e-4c87-bc32-d06dc739cd38` | 1.247569 | $7.80 | SELECT: How often do pages opt into Incremental Font Transfer (IFT), by signal, and which pages ar |
| 2026-08-04 03:18:09 | `c7053438-ec41-4e33-be05-a6453212a25f` | 1.218263 | $7.61 | SELECT: Which families are popular in CSS? |

## Files

- Every job, one row each: `expenses/bigquery-jobs-itemized.csv`
- One row per day: `expenses/bigquery-daily-summary.csv`

## Caveats

- The 1 TiB monthly free tier is shared across the whole billing account, so the net-of-free figure is correct only if nothing else on the account used queries in those months.
- Storage is accruing at about $56 per 30 days while the 68 tables stay, 2.4 TiB in all. It will continue until tables are deleted or expire. The two large tables are `pruned_css` and `font_requests`.
- Job times are UTC. Dates near midnight may fall on the previous or next local day.
- The project's finish plan of 2026-09 records "only spend ~$6". That predates the 2026-10-01 query that billed $106.72, the 2026-10-21 coverage queries, and the follow-up queries of 2026-10-24 and 2026-10-25.
