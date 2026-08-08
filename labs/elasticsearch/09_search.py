from pathlib import Path
import sys
import argparse

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from labs.elasticsearch.lab_impl import run_search


def main():
    parser = argparse.ArgumentParser(description="Search the Elasticsearch lab index for a query string.")
    parser.add_argument("query", help="Query string to search for")
    parser.add_argument("--top", type=int, default=10, help="Number of top results to return")
    args = parser.parse_args()
    run_search(args.query, top_k=args.top)


if __name__ == "__main__":
    main()
