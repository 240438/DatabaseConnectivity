from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from labs.common.config_loader import ConfigError, load_db_config


STUDENT_ID = 1001
TABLE_NAME = "students"


def _connect():
    config = load_db_config(
        "cassandra",
        "CASSANDRA",
        ["hosts", "port", "keyspace"],
        {
            "username": "",
            "password": "",
        },
    )

    hosts = [host.strip() for host in config["hosts"].split(",") if host.strip()]
    auth_provider = None
    if config["username"]:
        auth_provider = PlainTextAuthProvider(config["username"], config["password"])

    cluster = Cluster(contact_points=hosts, port=int(config["port"]), auth_provider=auth_provider)
    session = cluster.connect()
    return cluster, session, config["keyspace"]


def _ensure_schema(session, keyspace: str) -> None:
    session.execute(
        f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
        "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
    )
    session.set_keyspace(keyspace)
    session.execute(
        f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id int PRIMARY KEY, name text, course text)"
    )


def run_connect() -> None:
    cluster = None
    try:
        cluster, session, _ = _connect()
        row = session.execute("SELECT release_version FROM system.local").one()
        print(f"✅ Connected to Cassandra successfully (version: {row.release_version}).")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ Cassandra connection failed: {exc}")
    finally:
        if cluster:
            cluster.shutdown()


def run_create() -> None:
    cluster = None
    try:
        cluster, session, keyspace = _connect()
        _ensure_schema(session, keyspace)
        session.execute(
            f"INSERT INTO {TABLE_NAME} (id, name, course) VALUES (%s, %s, %s)",
            (STUDENT_ID, "Asha", "DB Basics"),
        )
        print(f"✅ Created seed row with id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ CREATE failed: {exc}")
    finally:
        if cluster:
            cluster.shutdown()


def run_read() -> None:
    cluster = None
    try:
        cluster, session, keyspace = _connect()
        _ensure_schema(session, keyspace)
        row = session.execute(
            f"SELECT id, name, course FROM {TABLE_NAME} WHERE id = %s",
            (STUDENT_ID,),
        ).one()
        print(f"✅ READ result: {row}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ READ failed: {exc}")
    finally:
        if cluster:
            cluster.shutdown()


def run_update() -> None:
    cluster = None
    try:
        cluster, session, keyspace = _connect()
        _ensure_schema(session, keyspace)
        before = session.execute(
            f"SELECT id, name, course FROM {TABLE_NAME} WHERE id = %s",
            (STUDENT_ID,),
        ).one()
        session.execute(
            f"UPDATE {TABLE_NAME} SET course = %s WHERE id = %s",
            ("Advanced Databases", STUDENT_ID),
        )
        after = session.execute(
            f"SELECT id, name, course FROM {TABLE_NAME} WHERE id = %s",
            (STUDENT_ID,),
        ).one()
        print(f"✅ UPDATE before: {before}")
        print(f"✅ UPDATE after : {after}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ UPDATE failed: {exc}")
    finally:
        if cluster:
            cluster.shutdown()


def run_delete() -> None:
    cluster = None
    try:
        cluster, session, keyspace = _connect()
        _ensure_schema(session, keyspace)
        session.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (STUDENT_ID,))
        print(f"✅ Deleted row with id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ DELETE failed: {exc}")
    finally:
        if cluster:
            cluster.shutdown()


def run_verify() -> None:
    cluster = None
    try:
        cluster, session, keyspace = _connect()
        _ensure_schema(session, keyspace)
        row = session.execute(f"SELECT id FROM {TABLE_NAME} WHERE id = %s", (STUDENT_ID,)).one()
        if row is None:
            print("✅ VERIFY passed: row is absent as expected.")
        else:
            print(f"❌ VERIFY failed: row still exists -> {row}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ VERIFY failed: {exc}")
    finally:
        if cluster:
            cluster.shutdown()
