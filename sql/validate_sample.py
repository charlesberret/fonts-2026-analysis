#!/usr/bin/env python
"""Validate font queries against HTTP Archive 10k sample tables.

The full `httparchive.crawl.*` tables cost ~$158 per query to scan on-demand.
The `httparchive.sample_data.*_10k` tables share the same schema but cost
fractions of a cent, so they are ideal for confirming a query compiles and
returns sensible output before spending real money on the full crawl.

This harness rewrites crawl table references to their sample equivalents,
runs each query, and prints the scan size, row count, and a result preview.

Usage:
    python validate_sample.py performance/styles_unicode_range.sql
    python validate_sample.py            # all queries
"""

import argparse
import re
from pathlib import Path

import google.auth  # pylint: disable=import-error
from google.cloud import bigquery  # pylint: disable=import-error

PROJECT_ID = "fonts-data-analysis"

# The crawl snapshot the sample tables are drawn from.
SAMPLE_DATE = "2026-07-01"

# Map full crawl tables to their 10k-sample equivalents.
SUBSTITUTIONS = {
    "httparchive.crawl.parsed_css": "httparchive.sample_data.parsed_css_10k",
    "httparchive.crawl.requests": "httparchive.sample_data.requests_10k",
    "httparchive.crawl.pages": "httparchive.sample_data.pages_10k",
}

QUERY_PARAMETERS = [
    bigquery.ScalarQueryParameter("date", "DATE", SAMPLE_DATE),
    bigquery.ArrayQueryParameter("dates", "DATE", [SAMPLE_DATE]),
    bigquery.ScalarQueryParameter("precision", "INT64", 4),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="*", default=["*/*.sql"])
    arguments = parser.parse_args()

    paths = sorted(
        path
        for pattern in arguments.path
        for path in Path(".").glob(pattern)
        if path.suffix == ".sql"
    )

    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

    for path in paths:
        _validate(client, path)


def _validate(client: bigquery.Client, path: Path) -> None:
    query = _rewrite(_query_read(path))
    print(f"\n=== {path} ===")
    try:
        config = bigquery.QueryJobConfig(
            query_parameters=QUERY_PARAMETERS,
            use_query_cache=True,
        )
        job = client.query(query, job_config=config)
        rows = list(job.result())
        scanned_gb = (job.total_bytes_processed or 0) / 1024**3
        print(f"  scanned {scanned_gb:.3f} GB (~${scanned_gb / 1024 * 5:.4f}), "
              f"{len(rows)} rows")
        if rows:
            columns = list(rows[0].keys())
            print("  columns:", columns)
            for row in rows[:8]:
                print("   ", dict(row))
    except Exception as error:  # pylint: disable=broad-except
        print("  FAILED:", str(error).splitlines()[0])


def _rewrite(query: str) -> str:
    for full, sample in SUBSTITUTIONS.items():
        query = query.replace(full, sample)
    return query


def _query_read(path: Path) -> str:
    lines = []
    for line in path.read_text().splitlines():
        match = re.search(r"^-- INCLUDE .*/([^/]+)\.sql$", line)
        if match:
            (name,) = match.groups()
            lines.extend(Path(f"{name}.sql").read_text().splitlines())
        else:
            lines.append(line)
    return "\n".join(lines)


if __name__ == "__main__":
    main()
