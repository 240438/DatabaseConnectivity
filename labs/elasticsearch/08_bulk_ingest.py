"""08_bulk_ingest.py - bulk ingest JSONL file into Elasticsearch index

Run order number: 08
Usage: python labs/elasticsearch/08_bulk_ingest.py path/to/file.json
"""
from pathlib import Path
import sys
import argparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from labs.elasticsearch.lab_impl import run_bulk_ingest


def main():
    parser = argparse.ArgumentParser(description="Bulk ingest JSONL file into Elasticsearch index (lab).")
    parser.add_argument("file", help="Path to JSONL file to ingest")
    args = parser.parse_args()
    run_bulk_ingest(args.file)


if __name__ == "__main__":
    main()
