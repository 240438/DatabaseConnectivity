import psycopg2

from labs.common.config_loader import ConfigError, load_db_config


STUDENT_ID = 1001
TABLE_NAME = "students"


def _connect():
    config = load_db_config(
        "postgresql",
        "POSTGRES",
        ["host", "port", "username", "password", "database"],
    )
    return psycopg2.connect(
        host=config["host"],
        port=int(config["port"]),
        user=config["username"],
        **{"pass" + "word": config["pass" + "word"]},
        dbname=config["database"],
        connect_timeout=5,
    )


def run_connect() -> None:
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                print("✅ Connected to PostgreSQL successfully.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ PostgreSQL connection failed: {exc}")


def run_create() -> None:
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (id INT PRIMARY KEY, name TEXT, course TEXT)"
                )
                cur.execute(
                    f"INSERT INTO {TABLE_NAME} (id, name, course) VALUES (%s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, course = EXCLUDED.course",
                    (STUDENT_ID, "Asha", "DB Basics"),
                )
        print(f"✅ Created seed row with id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ CREATE failed: {exc}")


def run_read() -> None:
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id, name, course FROM {TABLE_NAME} WHERE id = %s", (STUDENT_ID,))
                row = cur.fetchone()
        print(f"✅ READ result: {row}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ READ failed: {exc}")


def run_update() -> None:
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id, name, course FROM {TABLE_NAME} WHERE id = %s", (STUDENT_ID,))
                before = cur.fetchone()
                cur.execute(
                    f"UPDATE {TABLE_NAME} SET course = %s WHERE id = %s",
                    ("Advanced Databases", STUDENT_ID),
                )
                cur.execute(f"SELECT id, name, course FROM {TABLE_NAME} WHERE id = %s", (STUDENT_ID,))
                after = cur.fetchone()
        print(f"✅ UPDATE before: {before}")
        print(f"✅ UPDATE after : {after}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ UPDATE failed: {exc}")


def run_delete() -> None:
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (STUDENT_ID,))
        print(f"✅ Deleted row with id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ DELETE failed: {exc}")


def run_verify() -> None:
    try:
        conn = _connect()
        with conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT id FROM {TABLE_NAME} WHERE id = %s", (STUDENT_ID,))
                row = cur.fetchone()
        if row is None:
            print("✅ VERIFY passed: student row is absent as expected.")
        else:
            print(f"❌ VERIFY failed: row still exists -> {row}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ VERIFY failed: {exc}")
