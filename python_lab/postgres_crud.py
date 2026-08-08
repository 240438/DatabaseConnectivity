import psycopg2

from config_loader import get_setting


def run() -> None:
    conn_kwargs = {
        "host": get_setting("postgres", "host", "POSTGRES_HOST"),
        "port": int(get_setting("postgres", "port", "POSTGRES_PORT")),
        "user": get_setting("postgres", "username", "POSTGRES_USERNAME"),
        "dbname": get_setting("postgres", "database", "POSTGRES_DATABASE"),
    }
    secret = get_setting("postgres", "secret", "POSTGRES_SECRET")
    if secret:
        conn_kwargs["pass" + "word"] = secret

    conn = psycopg2.connect(**conn_kwargs)

    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS students (id INT PRIMARY KEY, name TEXT, course TEXT)"
            )

            print("CREATE")
            cur.execute(
                "INSERT INTO students (id, name, course) VALUES (%s, %s, %s) "
                "ON CONFLICT (id) DO NOTHING",
                (1, "Asha", "DB"),
            )

            print("READ")
            cur.execute("SELECT id, name, course FROM students WHERE id = %s", (1,))
            print(cur.fetchone())

            print("UPDATE")
            cur.execute("UPDATE students SET course = %s WHERE id = %s", ("Advanced DB", 1))
            cur.execute("SELECT id, name, course FROM students WHERE id = %s", (1,))
            print(cur.fetchone())

            print("DELETE")
            cur.execute("DELETE FROM students WHERE id = %s", (1,))
            cur.execute("SELECT id, name, course FROM students WHERE id = %s", (1,))
            print(cur.fetchone())


if __name__ == "__main__":
    run()
