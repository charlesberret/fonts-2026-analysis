#!/usr/bin/env python
"""Dry-run every query against a real crawl date to project the full-run bill.

Dry runs are free. This sums the bytes each query WOULD scan against the full
`httparchive.crawl.*` tables, grouped by the primary table each query hits, so
we can see the true on-demand cost before spending anything.
"""

import re
from pathlib import Path

import google.auth  # pylint: disable=import-error
from google.cloud import bigquery  # pylint: disable=import-error

PROJECT_ID = "fonts-data-analysis"
# Use a real crawl date (2025) so the dry run sees actual data volumes.
REAL_DATE = "2026-07-01"

PARAMS = [
    bigquery.ScalarQueryParameter("date", "DATE", REAL_DATE),
    bigquery.ArrayQueryParameter(
        "dates", "DATE",
        ["2022-07-01", "2023-07-01", "2024-07-01", "2025-07-01"],
    ),
    bigquery.ScalarQueryParameter("precision", "INT64", 4),
]


def read_query(path: Path) -> str:
    lines = []
    for line in path.read_text().splitlines():
        match = re.search(r"^-- INCLUDE .*/([^/]+)\.sql$", line)
        if match:
            (name,) = match.groups()
            lines.extend(Path(f"{name}.sql").read_text().splitlines())
        else:
            lines.append(line)
    return "\n".join(lines)


def primary_table(sql: str) -> str:
    if "crawl.parsed_css" in sql:
        return "parsed_css"
    if "crawl.requests" in sql:
        return "requests"
    if "crawl.pages" in sql:
        return "pages"
    return "other"


def main():
    creds, _ = google.auth.default()
    client = bigquery.Client(credentials=creds, project=PROJECT_ID)

    paths = sorted(
        p for p in Path(".").glob("*/*.sql") if p.suffix == ".sql"
    )

    by_table = {}
    grand_tb = 0.0
    rows = []
    for path in paths:
        sql = read_query(path)
        cfg = bigquery.QueryJobConfig(
            query_parameters=PARAMS, use_query_cache=False, dry_run=True
        )
        try:
            job = client.query(sql, job_config=cfg)
            tb = job.total_bytes_processed / 1024**4
        except Exception as error:  # pylint: disable=broad-except
            rows.append((str(path), -1, str(error).splitlines()[0]))
            continue
        table = primary_table(sql)
        by_table[table] = by_table.get(table, 0.0) + tb
        grand_tb += tb
        rows.append((str(path), tb, table))

    for path, tb, note in sorted(rows, key=lambda r: -r[1] if r[1] > 0 else 0):
        if tb < 0:
            print(f"  {path:60s}  DRY-RUN FAILED: {note}")
        else:
            print(f"  {path:60s}  {tb:8.4f} TB  ~${tb*5:8.2f}  [{note}]")

    print("\n=== by table ===")
    for table, tb in sorted(by_table.items(), key=lambda x: -x[1]):
        print(f"  {table:12s}  {tb:9.4f} TB  ~${tb*5:9.2f}")
    print(f"\n=== GRAND TOTAL: {grand_tb:.2f} TB  ~${grand_tb*5:,.2f} ===")


if __name__ == "__main__":
    main()
