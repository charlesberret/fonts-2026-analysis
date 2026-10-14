#!/usr/bin/env python

import argparse
import multiprocessing
import re
from pathlib import Path

import pandas as pd  # pylint: disable=import-error
import google.auth  # pylint: disable=import-error
from google.cloud import bigquery  # pylint: disable=import-error

# The project that owns the result dataset and is billed for queries.
PROJECT_ID = "fonts-data-analysis"

# The dataset where each query's results are persisted as a table, so the
# derived data can be re-queried for free without re-scanning the crawl.
DATASET_ID = "fonts_2026"

QUERY_PARAMETERS = [
    # The date of the crawl used for the analysis.
    bigquery.ScalarQueryParameter(
        "date",
        "DATE",
        "2026-07-01",  # Update to confirmed crawl date once known.
    ),
    # A set of dates for queries studying trends over time.
    bigquery.ArrayQueryParameter(
        "dates",
        "DATE",
        ["2022-07-01", "2023-07-01", "2024-07-01", "2025-07-01", "2026-07-01"],
    ),
    # The number of digits after the decimal point for formatting proportions.
    bigquery.ScalarQueryParameter(
        "precision",
        "INT64",
        4,
    ),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="*", default=["*/*.sql"])
    parser.add_argument("--no-dry-run", action="store_true")
    parser.add_argument("--workers", type=int, default=multiprocessing.cpu_count())
    arguments = parser.parse_args()

    paths = list(
        path
        for path in arguments.path
        for path in Path(".").glob(path)
        if path.suffix == ".sql"
    )
    width = max(len(str(path)) for path in paths) + 1

    tasks = [{"path": path, "dry_run": not arguments.no_dry_run} for path in paths]
    with multiprocessing.Pool(arguments.workers) as pool:
        for result in pool.imap_unordered(_process, tasks):
            task = result["task"]
            path = task["path"]
            if result["failures"]:
                messages = list(
                    map(
                        lambda failure: failure.splitlines()[0],
                        result["failures"],
                    )
                )
            elif result["successes"]:
                messages = result["successes"]
            else:
                messages = []
            if not messages:
                print(f"{str(path).ljust(width)}: skipped")
            elif len(messages) == 1:
                print(f"{str(path).ljust(width)}: {messages[0]}")
            else:
                print(f"{path}:")
                for message in messages:
                    print(f"  - {message}")


def _process(task: dict) -> dict:
    result = {"task": task, "failures": [], "successes": []}

    query = _query_read(task["path"])
    csv_path = task["path"].with_suffix(".csv")

    # If results are already cached locally, there is nothing to do.
    if csv_path.exists():
        return result

    try:
        if task["dry_run"]:
            size = _bigquery_estimate(query["content"])
            result["successes"].append(f"estimated {size:5.2f} TB")
        else:
            data = _bigquery_read(query["content"])
            data.to_csv(csv_path, index=False)
            table = _table_name(task["path"])
            _bigquery_load(data, table)
            result["successes"].append(
                f"wrote {csv_path} and {DATASET_ID}.{table} ({len(data)} rows)"
            )
    except Exception as error:
        result["failures"].append(str(error))

    return result


def _bigquery_estimate(query: str) -> float:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    config = bigquery.QueryJobConfig(
        query_parameters=QUERY_PARAMETERS,
        use_query_cache=False,
        dry_run=True,
    )
    job = client.query(query, job_config=config)
    return job.total_bytes_processed / 1024 / 1024 / 1024 / 1024


def _bigquery_read(query: str) -> pd.DataFrame:
    credentials, _ = google.auth.default()
    client = bigquery.Client(
        credentials=credentials,
        project=PROJECT_ID,
    )
    config = bigquery.QueryJobConfig(
        query_parameters=QUERY_PARAMETERS,
        use_query_cache=True,
    )
    job = client.query(query, job_config=config)
    return job.to_dataframe()


def _bigquery_load(data: pd.DataFrame, table: str) -> None:
    credentials, _ = google.auth.default()
    client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table}"
    config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(data, table_id, job_config=config)
    job.result()


def _table_name(path: Path) -> str:
    # e.g. performance/styles_unicode_range.sql -> performance__styles_unicode_range
    return f"{path.parent.name}__{path.stem}"


def _query_read(path: Path) -> dict:
    lines = []
    metadata = {}
    for line in path.read_text().splitlines():
        match = re.search(r"^-- (.+): (.+)$", line)
        if match:
            name, value = match.groups()
            metadata[name] = value
        match = re.search(r"^-- INCLUDE .*/([^/]+)\.sql$", line)
        if match:
            (name,) = match.groups()
            lines.extend(Path(f"{name}.sql").read_text().splitlines())
        else:
            lines.append(line)
    return {
        "content": "\n".join(lines),
        "metadata": metadata,
    }


if __name__ == "__main__":
    main()
