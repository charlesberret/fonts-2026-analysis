#!/usr/bin/env python
"""Run request-side font queries against materialized tables (no CSS).

Uses:
  fonts-data-analysis.fonts_2026.font_requests   (type=font, 2026-07-01)
  fonts-data-analysis.fonts_2026.root_pages      (all root pages, denominators)

@dates queries are allowed: QUERY_PARAMETERS pins @dates to [2026-07-01]
so multi-year SQL rewrites cleanly against the single-date materialize.

Skips:
  - queries that need crawl.parsed_css (CSS materialize separate)
  - materialize/*.sql

Special:
  - pages_link_relationship: crawl.pages (date=@date) + font_requests join

Usage:
  export CLOUDSDK_CORE_DISABLE_PROMPTS=1
  python execute_materialized.py              # dry-run estimates
  python execute_materialized.py --no-dry-run # write CSVs + result tables
  python execute_materialized.py --no-dry-run design/fonts_foundry.sql
  python execute_materialized.py --no-dry-run --force  # re-run even if CSV exists
"""

from __future__ import annotations

import argparse
import multiprocessing
import os
import re
import sys
from pathlib import Path

import google.auth  # pylint: disable=import-error
import pandas as pd  # pylint: disable=import-error
from google.cloud import bigquery  # pylint: disable=import-error

os.environ.setdefault("CLOUDSDK_CORE_DISABLE_PROMPTS", "1")

PROJECT_ID = "fonts-data-analysis"
DATASET_ID = "fonts_2026"
FONT_REQUESTS = f"`{PROJECT_ID}.{DATASET_ID}.font_requests`"
ROOT_PAGES = f"`{PROJECT_ID}.{DATASET_ID}.root_pages`"
CRAWL_REQUESTS = "`httparchive.crawl.requests`"

QUERY_PARAMETERS = [
    bigquery.ScalarQueryParameter("date", "DATE", "2026-07-01"),
    bigquery.ArrayQueryParameter(
        "dates", "DATE", ["2026-07-01"]
    ),  # multi-date skipped anyway
    bigquery.ScalarQueryParameter("precision", "INT64", 4),
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="*", default=["*/*.sql"])
    parser.add_argument("--no-dry-run", action="store_true")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-run even when a CSV already exists",
    )
    parser.add_argument(
        "--workers", type=int, default=min(4, multiprocessing.cpu_count())
    )
    args = parser.parse_args()

    paths = sorted(
        {
            p
            for pattern in args.path
            for p in Path(".").glob(pattern)
            if p.suffix == ".sql" and _is_eligible(p)
        }
    )
    if not paths:
        print("No eligible request-side queries found.")
        sys.exit(1)

    print(f"Eligible queries: {len(paths)}")
    print(f"Mode: {'EXECUTE' if args.no_dry_run else 'DRY-RUN'}")
    print()

    width = max(len(str(p)) for p in paths) + 1
    tasks = [
        {
            "path": p,
            "dry_run": not args.no_dry_run,
            "force": args.force,
        }
        for p in paths
    ]

    # Sequential if 1 worker; pool otherwise
    if args.workers <= 1:
        results = [_process(t) for t in tasks]
    else:
        with multiprocessing.Pool(args.workers) as pool:
            results = list(pool.imap_unordered(_process, tasks))

    ok = fail = skip = 0
    for result in sorted(results, key=lambda r: str(r["task"]["path"])):
        path = result["task"]["path"]
        if result.get("skipped"):
            print(f"{str(path).ljust(width)}: skipped ({result['skipped']})")
            skip += 1
        elif result["failures"]:
            msg = result["failures"][0].splitlines()[0]
            print(f"{str(path).ljust(width)}: FAIL {msg}")
            fail += 1
        else:
            print(f"{str(path).ljust(width)}: {result['successes'][0]}")
            ok += 1

    print()
    print(f"=== {ok} ok, {fail} fail, {skip} skipped ===")
    sys.exit(1 if fail else 0)


def _is_eligible(path: Path) -> bool:
    if path.parts[0] == "materialize":
        return False
    text = path.read_text()
    if "crawl.parsed_css" in text:
        return False
    # pages_link_relationship is handled specially (needs crawl.pages)
    if path.name == "pages_link_relationship.sql":
        return True
    if "httparchive.crawl.pages" in text:
        return False
    if "httparchive.crawl.requests" not in text and "crawl.requests" not in text:
        return False
    # @dates queries are OK: QUERY_PARAMETERS pins @dates to [2026-07-01]
    return True


def _process(task: dict) -> dict:
    result = {"task": task, "failures": [], "successes": [], "skipped": None}
    path: Path = task["path"]
    csv_path = path.with_suffix(".csv")

    if csv_path.exists() and not task["dry_run"] and not task.get("force"):
        result["skipped"] = "csv exists"
        return result

    try:
        raw = _query_read(path)
        sql = rewrite_to_materialized(raw, path)
        if task["dry_run"]:
            tb = _estimate(sql)
            result["successes"].append(f"estimated {tb:6.3f} TB  ~${tb * 5:6.2f}")
        else:
            data = _read(sql)
            data.to_csv(csv_path, index=False)
            table = f"{path.parent.name}__{path.stem}"
            _load(data, table)
            result["successes"].append(
                f"wrote {csv_path} + {DATASET_ID}.{table} ({len(data)} rows)"
            )
    except Exception as error:  # pylint: disable=broad-except
        result["failures"].append(str(error))
    return result


def rewrite_to_materialized(sql: str, path: Path) -> str:
    """Point request queries at font_requests / root_pages."""
    # Special: overall font usage needs both tables
    if path.name == "fonts.sql" and "IF(type = 'font'" in sql:
        return _rewrite_fonts_usage()

    if path.name == "pages_link_relationship.sql":
        return _rewrite_pages_link_relationship(sql)

    # Default: font detail from font_requests
    out = sql.replace(CRAWL_REQUESTS, FONT_REQUESTS)
    # Also bare form without backticks issues
    out = out.replace("httparchive.crawl.requests", f"{PROJECT_ID}.{DATASET_ID}.font_requests")

    # Page-denominator CTEs: no type='font' filter → root_pages
    out = _retarget_page_totals(out)
    return out


def _retarget_page_totals(sql: str) -> str:
    """Switch 'pages AS (...)' totals from font_requests → root_pages when not font-filtered."""

    # Flexible whitespace: pages AS ( SELECT ... FROM font_requests WHERE ... is_root_page ... )
    pattern = re.compile(
        r"(pages\s+AS\s*\(\s*"
        r"SELECT[\s\S]*?"
        r"FROM\s+)"
        + re.escape(FONT_REQUESTS)
        + r"(\s+WHERE[\s\S]*?\))",
        re.IGNORECASE,
    )

    def repl(match: re.Match) -> str:
        head, tail = match.group(1), match.group(2)
        # If this block filters type = font, keep font_requests
        if re.search(r"type\s*=\s*['\"]font['\"]", tail, re.I):
            return match.group(0)
        return head + ROOT_PAGES + tail

    return pattern.sub(repl, sql)


def _rewrite_fonts_usage() -> str:
    """performance/fonts.sql against materialize (July only)."""
    return f"""
SELECT
  date,
  client,
  count,
  total,
  ROUND(count / total, @precision) AS proportion
FROM (
  SELECT
    f.date,
    f.client,
    f.count,
    p.total
  FROM (
    SELECT
      date,
      client,
      COUNT(DISTINCT page) AS count
    FROM {FONT_REQUESTS}
    WHERE
      date = @date
      AND is_root_page
    GROUP BY
      date,
      client
  ) AS f
  JOIN (
    SELECT
      date,
      client,
      COUNT(DISTINCT page) AS total
    FROM {ROOT_PAGES}
    WHERE
      date = @date
      AND is_root_page
    GROUP BY
      date,
      client
  ) AS p
  USING (date, client)
)
ORDER BY
  date,
  client
"""


def _rewrite_pages_link_relationship(sql: str) -> str:
    """pages_link_relationship: crawl.pages for hints, font_requests for font URL join.

    Scans httparchive.crawl.pages for 2026-07-01 only (not free — dry-run first).
    Font side uses materialize so we do not rescan all requests.
    """
    out = sql.replace(CRAWL_REQUESTS, FONT_REQUESTS)
    out = out.replace(
        "httparchive.crawl.requests", f"{PROJECT_ID}.{DATASET_ID}.font_requests"
    )
    # Prefer single @date when query already uses @dates for pages
    out = re.sub(
        r"pages\.date\s+IN\s+UNNEST\s*\(\s*@dates\s*\)",
        "pages.date = @date",
        out,
        flags=re.I,
    )
    out = re.sub(
        r"requests\.date\s+IN\s+UNNEST\s*\(\s*@dates\s*\)",
        "requests.date = @date",
        out,
        flags=re.I,
    )
    out = re.sub(
        r"\bdate\s+IN\s+UNNEST\s*\(\s*@dates\s*\)",
        "date = @date",
        out,
        flags=re.I,
    )
    return out


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


def _estimate(sql: str) -> float:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    config = bigquery.QueryJobConfig(
        query_parameters=QUERY_PARAMETERS,
        use_query_cache=False,
        dry_run=True,
    )
    job = client.query(sql, job_config=config)
    return (job.total_bytes_processed or 0) / 1024**4


def _read(sql: str) -> pd.DataFrame:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    config = bigquery.QueryJobConfig(
        query_parameters=QUERY_PARAMETERS,
        use_query_cache=True,
    )
    job = client.query(sql, job_config=config)
    return job.to_dataframe()


def _load(data: pd.DataFrame, table: str) -> None:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table}"
    config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(data, table_id, job_config=config)
    job.result()


if __name__ == "__main__":
    main()
