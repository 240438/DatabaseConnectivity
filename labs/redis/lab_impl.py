import redis

from labs.common.config_loader import ConfigError, load_db_config


STUDENT_KEY = "student:1001"


def _connect() -> redis.Redis:
    config = load_db_config(
        "redis",
        "REDIS",
        ["host", "port"],
        {
            "username": "",
            "password": "",
        },
    )
    kwargs = {
        "host": config["host"],
        "port": int(config["port"]),
        "decode_responses": True,
    }
    if config["username"]:
        kwargs["username"] = config["username"]
    if config["password"]:
        kwargs["password"] = config["password"]
    return redis.Redis(**kwargs)


def run_connect() -> None:
    try:
        client = _connect()
        client.ping()
        print("✅ Connected to Redis successfully.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ Redis connection failed: {exc}")


def run_create() -> None:
    try:
        client = _connect()
        client.hset(STUDENT_KEY, mapping={"name": "Asha", "course": "DB Basics"})
        print(f"✅ Created seed hash at key={STUDENT_KEY}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ CREATE failed: {exc}")


def run_read() -> None:
    try:
        client = _connect()
        data = client.hgetall(STUDENT_KEY)
        print(f"✅ READ result: {data}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ READ failed: {exc}")


def run_update() -> None:
    try:
        client = _connect()
        before = client.hgetall(STUDENT_KEY)
        client.hset(STUDENT_KEY, mapping={"course": "Advanced Databases"})
        after = client.hgetall(STUDENT_KEY)
        print(f"✅ UPDATE before: {before}")
        print(f"✅ UPDATE after : {after}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ UPDATE failed: {exc}")


def run_delete() -> None:
    try:
        client = _connect()
        client.delete(STUDENT_KEY)
        print(f"✅ Deleted key={STUDENT_KEY}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ DELETE failed: {exc}")


def run_verify() -> None:
    try:
        client = _connect()
        exists = client.exists(STUDENT_KEY)
        if exists == 0:
            print("✅ VERIFY passed: key is absent as expected.")
        else:
            print("❌ VERIFY failed: key still exists.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ VERIFY failed: {exc}")
