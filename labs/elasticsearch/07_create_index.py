"""07_create_index.py - create the configured Elasticsearch index (idempotent)

Run order number: 07
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from labs.elasticsearch.lab_impl import run_create_index


if __name__ == "__main__":
    run_create_index()
