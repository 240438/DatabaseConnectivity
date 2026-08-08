from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster

from config_loader import get_setting


def run() -> None:
    hosts = [h.strip() for h in get_setting("cassandra", "hosts", "CASSANDRA_HOSTS").split(",")]
    port = int(get_setting("cassandra", "port", "CASSANDRA_PORT"))
    username = get_setting("cassandra", "username", "CASSANDRA_USERNAME")
    secret = get_setting("cassandra", "secret", "CASSANDRA_SECRET")

    auth_provider = None
    if username:
        auth_provider = PlainTextAuthProvider(username, secret)

    cluster = Cluster(contact_points=hosts, port=port, auth_provider=auth_provider)
    session = cluster.connect()

    keyspace = get_setting("cassandra", "keyspace", "CASSANDRA_KEYSPACE")
    session.execute(
        f"CREATE KEYSPACE IF NOT EXISTS {keyspace} "
        "WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
    )
    session.set_keyspace(keyspace)

    session.execute(
        "CREATE TABLE IF NOT EXISTS students (id int PRIMARY KEY, name text, course text)"
    )

    print("CREATE")
    session.execute(
        "INSERT INTO students (id, name, course) VALUES (%s, %s, %s)",
        (1, "Asha", "DB"),
    )

    print("READ")
    row = session.execute("SELECT id, name, course FROM students WHERE id=%s", (1,)).one()
    print(row)

    print("UPDATE")
    session.execute("UPDATE students SET course=%s WHERE id=%s", ("Advanced DB", 1))
    print(session.execute("SELECT id, name, course FROM students WHERE id=%s", (1,)).one())

    print("DELETE")
    session.execute("DELETE FROM students WHERE id=%s", (1,))
    print(session.execute("SELECT id, name, course FROM students WHERE id=%s", (1,)).one())

    cluster.shutdown()


if __name__ == "__main__":
    run()
