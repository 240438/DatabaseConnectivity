from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from labs.cassandra.lab_impl import run_delete


if __name__ == "__main__":
    run_delete()
