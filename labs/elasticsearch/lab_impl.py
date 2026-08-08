from elasticsearch import Elasticsearch, NotFoundError

from labs.common.config_loader import ConfigError, load_db_config


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
