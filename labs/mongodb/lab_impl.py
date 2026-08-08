from pymongo import MongoClient

from labs.common.config_loader import ConfigError, load_db_config


STUDENT_ID = "student-1001"
COLLECTION_NAME = "students"


def _connect():
    config = load_db_config(
        "mongodb",
        "MONGODB",
        ["host", "port", "database"],
        {
            "username": "",
            "password": "",
            "auth_source": "admin",
        },
    )

    if config["username"]:
        uri = (
            f"mongodb://{config['username']}:{config['password']}@{config['host']}:{config['port']}"
            f"/?authSource={config['auth_source']}"
        )
    else:
        uri = f"mongodb://{config['host']}:{config['port']}/"

    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    db = client[config["database"]]
    return client, db[COLLECTION_NAME]


def run_connect() -> None:
    try:
        client, _ = _connect()
        client.admin.command("ping")
        print("✅ Connected to MongoDB successfully.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ MongoDB connection failed: {exc}")


def run_create() -> None:
    try:
        _, collection = _connect()
        collection.replace_one(
            {"_id": STUDENT_ID},
            {"_id": STUDENT_ID, "name": "Asha", "course": "DB Basics"},
            upsert=True,
        )
        print(f"✅ Created seed document with _id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ CREATE failed: {exc}")


def run_read() -> None:
    try:
        _, collection = _connect()
        document = collection.find_one({"_id": STUDENT_ID})
        print(f"✅ READ result: {document}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ READ failed: {exc}")


def run_update() -> None:
    try:
        _, collection = _connect()
        before = collection.find_one({"_id": STUDENT_ID})
        collection.update_one({"_id": STUDENT_ID}, {"$set": {"course": "Advanced Databases"}})
        after = collection.find_one({"_id": STUDENT_ID})
        print(f"✅ UPDATE before: {before}")
        print(f"✅ UPDATE after : {after}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ UPDATE failed: {exc}")


def run_delete() -> None:
    try:
        _, collection = _connect()
        collection.delete_one({"_id": STUDENT_ID})
        print(f"✅ Deleted document with _id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ DELETE failed: {exc}")


def run_verify() -> None:
    try:
        _, collection = _connect()
        exists = collection.find_one({"_id": STUDENT_ID}) is not None
        if not exists:
            print("✅ VERIFY passed: document is absent as expected.")
        else:
            print("❌ VERIFY failed: document still exists.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ VERIFY failed: {exc}")
