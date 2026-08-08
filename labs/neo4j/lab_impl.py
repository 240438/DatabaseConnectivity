from neo4j import GraphDatabase

from labs.common.config_loader import ConfigError, load_db_config


STUDENT_ID = 1001


def _connect():
    config = load_db_config(
        "neo4j",
        "NEO4J",
        ["uri", "username", "password"],
        {
            "database": "neo4j",
        },
    )
    driver = GraphDatabase.driver(config["uri"], auth=(config["username"], config["password"]))
    return driver, config["database"]


def run_connect() -> None:
    try:
        driver, _ = _connect()
        driver.verify_connectivity()
        print("✅ Connected to Neo4j successfully.")
        driver.close()
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ Neo4j connection failed: {exc}")


def run_create() -> None:
    try:
        driver, database = _connect()
        with driver.session(database=database) as session:
            session.run(
                "MERGE (s:Student {id: $id}) SET s.name = $name, s.course = $course",
                id=STUDENT_ID,
                name="Asha",
                course="DB Basics",
            )
        driver.close()
        print(f"✅ Created/merged Student node with id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ CREATE failed: {exc}")


def run_read() -> None:
    try:
        driver, database = _connect()
        with driver.session(database=database) as session:
            record = session.run(
                "MATCH (s:Student {id: $id}) RETURN s.id AS id, s.name AS name, s.course AS course",
                id=STUDENT_ID,
            ).single()
        driver.close()
        print(f"✅ READ result: {record.data() if record else None}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ READ failed: {exc}")


def run_update() -> None:
    try:
        driver, database = _connect()
        with driver.session(database=database) as session:
            before = session.run(
                "MATCH (s:Student {id: $id}) RETURN s.id AS id, s.name AS name, s.course AS course",
                id=STUDENT_ID,
            ).single()
            session.run(
                "MATCH (s:Student {id: $id}) SET s.course = $course",
                id=STUDENT_ID,
                course="Advanced Databases",
            )
            after = session.run(
                "MATCH (s:Student {id: $id}) RETURN s.id AS id, s.name AS name, s.course AS course",
                id=STUDENT_ID,
            ).single()
        driver.close()
        print(f"✅ UPDATE before: {before.data() if before else None}")
        print(f"✅ UPDATE after : {after.data() if after else None}")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ UPDATE failed: {exc}")


def run_delete() -> None:
    try:
        driver, database = _connect()
        with driver.session(database=database) as session:
            session.run("MATCH (s:Student {id: $id}) DETACH DELETE s", id=STUDENT_ID)
        driver.close()
        print(f"✅ Deleted Student node with id={STUDENT_ID}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ DELETE failed: {exc}")


def run_verify() -> None:
    try:
        driver, database = _connect()
        with driver.session(database=database) as session:
            count = session.run(
                "MATCH (s:Student {id: $id}) RETURN count(s) AS count",
                id=STUDENT_ID,
            ).single()["count"]
        driver.close()
        if count == 0:
            print("✅ VERIFY passed: node is absent as expected.")
        else:
            print(f"❌ VERIFY failed: node count is {count}.")
    except ConfigError as exc:
        print(f"❌ Configuration error: {exc}")
    except Exception as exc:
        print(f"❌ VERIFY failed: {exc}")
