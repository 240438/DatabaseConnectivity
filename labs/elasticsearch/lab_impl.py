from elasticsearch import Elasticsearch, NotFoundError  # type: ignore
from labs.common.config_loader import ConfigError, load_db_config
import os
import json

STUDENT_ID = "student-1001"


def _connect() -> tuple[Elasticsearch, str]:
    config = load_db_config(
        "elasticsearch",
        "ELASTICSEARCH",
        ["host", "index"],
        {
            "username": "",
            "password": "",
        },
    )
    auth = None
    if config["username"]:
        auth = (config["username"], config["password"])
    client = Elasticsearch(hosts=[config["host"]], basic_auth=auth)
    return client, config["index"]


def run_connect() -> None:
    try:
        client, _ = _connect()
        if client.ping():
            print("✅ Connected to Elasticsearch successfully.")
        else:
            print("❌ Elasticsearch ping failed. Service may not be ready yet.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ Elasticsearch connection failed: {exc}")


def run_create() -> None:
    try:
        client, index = _connect()
        client.index(
            index=index,
            id=STUDENT_ID,
            document={"name": "Asha", "course": "DB Basics"},
            refresh=True,
        )
        print(f"✅ Created seed document with id={STUDENT_ID} in index={index}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ CREATE failed: {exc}")


def run_read() -> None:
    try:
        client, index = _connect()
        result = client.get(index=index, id=STUDENT_ID)
        print(f"✅ READ result: {result['_source']}")
    except NotFoundError:
        print("❌ READ result: document not found.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ READ failed: {exc}")


def run_update() -> None:
    try:
        client, index = _connect()
        before = client.get(index=index, id=STUDENT_ID)['_source']
        client.update(
            index=index,
            id=STUDENT_ID,
            doc={"course": "Advanced Databases"},
            refresh=True,
        )
        after = client.get(index=index, id=STUDENT_ID)['_source']
        print(f"✅ UPDATE before: {before}")
        print(f"✅ UPDATE after : {after}")
    except NotFoundError:
        print("❌ UPDATE failed: create the document first using 02_create.py.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ UPDATE failed: {exc}")


def run_delete() -> None:
    try:
        client, index = _connect()
        client.delete(index=index, id=STUDENT_ID, refresh=True, ignore=[404])
        print(f"✅ Deleted document with id={STUDENT_ID} from index={index}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ DELETE failed: {exc}")


def run_verify() -> None:
    try:
        client, index = _connect()
        exists = client.exists(index=index, id=STUDENT_ID)
        if not exists:
            print("✅ VERIFY passed: document is absent as expected.")
        else:
            print("❌ VERIFY failed: document still exists.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ VERIFY failed: {exc}")


# New utilities: create_index, bulk_ingest, search

def run_create_index() -> None:
    try:
        client, index = _connect()
        try:
            client.indices.create(index=index, ignore=400)
            print(f"✅ Index '{index}' created (or already exists).")
        except AttributeError:
            print(f"ℹ️ Client has no indices.create; assuming index '{index}' is available.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ CREATE INDEX failed: {exc}")


def run_bulk_ingest(filepath: str) -> None:
    """Bulk ingest JSONL file into the configured index.

    Expected JSONL lines: either:
      {"id": "doc1", "document": { ... }}
    or
      {"id": "doc1", "text": "full text", "field": "value"}
    """
    try:
        client, index = _connect()

        if not os.path.exists(filepath):
            print(f"❌ Bulk file not found: {filepath}")
            return

        imported = 0
        with open(filepath, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception as exc:
                    print(f"⚠️ Skipping invalid JSON line: {exc}")
                    continue

                doc_id = obj.get("id")
                document = obj.get("document") or obj
                if doc_id is None:
                    print("⚠️ Skipping line without 'id' field.")
                    continue

                if document is obj:
                    document = dict(obj)
                    document.pop("id", None)

                client.index(index=index, id=doc_id, document=document, refresh=False)
                imported += 1

        print(f"✅ Bulk ingest completed. Imported {imported} documents into index='{index}'.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ BULK INGEST failed: {exc}")


def run_search(query: str, top_k: int = 10) -> None:
    try:
        client, index = _connect()
        resp = client.search(index=index, query={"query_string": {"query": query}}, size=top_k)
        hits = resp.get("hits", {}).get("hits", [])
        if not hits:
            print("No results.")
            return
        for h in hits:
            doc_id = h.get("_id")
            score = h.get("_score")
            src = h.get("_source")
            print(f"- {doc_id} (score={score:.4f}): {src}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ SEARCH failed: {exc}")
