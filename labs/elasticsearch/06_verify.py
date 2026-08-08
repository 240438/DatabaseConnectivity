from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from labs.elasticsearch.lab_impl import run_verify


if __name__ == "__main__":
    run_verify()
