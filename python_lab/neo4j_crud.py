from neo4j import GraphDatabase

from config_loader import get_setting


def run() -> None:
    uri = get_setting("neo4j", "uri", "NEO4J_URI")
    username = get_setting("neo4j", "username", "NEO4J_USERNAME")
    secret = get_setting("neo4j", "secret", "NEO4J_SECRET")

    driver = GraphDatabase.driver(uri, auth=(username, secret))

    with driver.session() as session:
        print("CREATE")
        session.run(
            "MERGE (s:Student {id: $id}) SET s.name = $name, s.course = $course",
            id=1,
            name="Asha",
            course="DB",
        )

        print("READ")
        record = session.run("MATCH (s:Student {id: $id}) RETURN s", id=1).single()
        print(record["s"] if record else None)

        print("UPDATE")
        session.run(
            "MATCH (s:Student {id: $id}) SET s.course = $course",
            id=1,
            course="Advanced DB",
        )
        record = session.run("MATCH (s:Student {id: $id}) RETURN s", id=1).single()
        print(record["s"] if record else None)

        print("DELETE")
        session.run("MATCH (s:Student {id: $id}) DETACH DELETE s", id=1)
        record = session.run("MATCH (s:Student {id: $id}) RETURN s", id=1).single()
        print(record)

    driver.close()


if __name__ == "__main__":
    run()
