#!/usr/bin/env python
"""Prove the pruned CSS table yields identical results to raw parsed_css.

For each parsed_css-based query, run it twice on the sample:
  - baseline: against raw httparchive.sample_data.parsed_css_10k
  - pruned:   against fonts-data-analysis.fonts_2026.sample_pruned
and compare the result rows exactly. Any mismatch means the pruning UDF dropped
something a query needed. All-match means the pruned approach is safe to run on
the full crawl with the queries unchanged.

Before comparing queries, verifies that sample_pruned's date partition matches
SAMPLE_DATE (avoids the June-table-vs-July-filter false-empty pattern).
"""

import re
import sys
from collections import Counter
from pathlib import Path

# Line-buffer stdout so `tee` shows progress during long runs.
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

import google.auth  # pylint: disable=import-error
from google.cloud import bigquery  # pylint: disable=import-error

PROJECT_ID = "fonts-data-analysis"
SAMPLE_DATE = "2026-07-01"

RAW_CSS = "httparchive.sample_data.parsed_css_10k"
PRUNED_CSS = "fonts-data-analysis.fonts_2026.sample_pruned"
RAW_REQUESTS = "httparchive.sample_data.requests_10k"

QUERY_PARAMETERS = [
    bigquery.ScalarQueryParameter("date", "DATE", SAMPLE_DATE),
    bigquery.ArrayQueryParameter("dates", "DATE", [SAMPLE_DATE]),
    bigquery.ScalarQueryParameter("precision", "INT64", 4),
]


def read_query(path: Path) -> str:
    lines = []
    for line in path.read_text().splitlines():
        m = re.search(r"^-- INCLUDE .*/([^/]+)\.sql$", line)
        if m:
            lines.extend(Path(m.group(1) + ".sql").read_text().splitlines())
        else:
            lines.append(line)
    return "\n".join(lines)


def run(client, sql):
    # Never cache: a prior run against a stale sample_pruned (wrong month)
    # must not keep returning empty result sets after rebuild.
    cfg = bigquery.QueryJobConfig(
        query_parameters=QUERY_PARAMETERS,
        use_query_cache=False,
    )
    rows = list(client.query(sql, job_config=cfg).result())
    # multiset of row tuples — order-independent and NULL-safe (no sorting)
    return Counter(tuple(r.values()) for r in rows)


def assert_pruned_table_fresh(client: bigquery.Client) -> None:
    """Fail fast if sample_pruned is missing or not for SAMPLE_DATE."""
    sql = f"""
    SELECT
      CAST(date AS STRING) AS date,
      COUNT(*) AS n
    FROM `{PRUNED_CSS}`
    GROUP BY date
    ORDER BY date
    """
    rows = list(client.query(sql).result())
    if not rows:
        print(f"FATAL: `{PRUNED_CSS}` is empty. Rebuild with materialize/rebuild_sample_pruned.sql")
        sys.exit(2)
    dates = {r["date"]: r["n"] for r in rows}
    print(f"sample_pruned partitions: {dates}")
    print(f"SAMPLE_DATE={SAMPLE_DATE}")
    if SAMPLE_DATE not in dates:
        print(
            f"FATAL: sample_pruned has no rows for {SAMPLE_DATE}. "
            f"Rebuild: bq query --use_legacy_sql=false < materialize/rebuild_sample_pruned.sql"
        )
        sys.exit(2)
    extra = set(dates) - {SAMPLE_DATE}
    if extra:
        print(f"NOTE: sample_pruned also has other dates (ignored): {extra}")
    print(f"OK: sample_pruned has {dates[SAMPLE_DATE]} rows for {SAMPLE_DATE}\n")


def main():
    creds, _ = google.auth.default()
    client = bigquery.Client(credentials=creds, project=PROJECT_ID)

    assert_pruned_table_fresh(client)

    paths = sorted(
        p for p in Path(".").glob("*/*.sql")
        if "crawl.parsed_css" in p.read_text()
    )

    ok, bad = 0, 0
    for path in paths:
        base_sql = read_query(path)
        raw = base_sql.replace("httparchive.crawl.parsed_css", RAW_CSS) \
                      .replace("httparchive.crawl.requests", RAW_REQUESTS)
        pruned = base_sql.replace("httparchive.crawl.parsed_css", PRUNED_CSS) \
                         .replace("httparchive.crawl.requests", RAW_REQUESTS)
        try:
            r_raw = run(client, raw)
            r_pruned = run(client, pruned)
        except Exception as e:  # pylint: disable=broad-except
            print(f"  ERROR  {path}: {str(e).splitlines()[0]}")
            bad += 1
            continue
        if r_raw == r_pruned:
            print(f"  MATCH  {path}  ({sum(r_raw.values())} rows)")
            ok += 1
        else:
            only_raw = r_raw - r_pruned
            only_pruned = r_pruned - r_raw
            # Flag the false-empty pattern explicitly.
            if sum(r_pruned.values()) == 0 and sum(r_raw.values()) > 0:
                print(
                    f"  EMPTY-PRUNED {path}: raw has {sum(r_raw.values())} rows, "
                    f"pruned has 0 (table/date mismatch or stale cache — not a prune logic bug)"
                )
            else:
                print(
                    f"  DIFFER {path}: {sum(only_raw.values())} rows only in raw, "
                    f"{sum(only_pruned.values())} only in pruned"
                )
            for row in list(only_raw)[:5]:
                print(f"      only raw:    {row}")
            for row in list(only_pruned)[:5]:
                print(f"      only pruned: {row}")
            bad += 1

    print(f"\n=== {ok} match, {bad} differ/error ===")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
