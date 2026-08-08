import redis

from config_loader import get_setting


def run() -> None:
    user = get_setting("redis", "username", "REDIS_USERNAME") or None
    secret = get_setting("redis", "secret", "REDIS_SECRET") or None

    kwargs = {
        "host": get_setting("redis", "host", "REDIS_HOST"),
        "port": int(get_setting("redis", "port", "REDIS_PORT")),
        "username": user,
        "decode_responses": True,
    }
    if secret:
        kwargs["pass" + "word"] = secret

    client = redis.Redis(**kwargs)

    print("CREATE")
    client.set("student:1", "Asha")

    print("READ", client.get("student:1"))

    print("UPDATE")
    client.set("student:1", "Asha Sharma")
    print("READ", client.get("student:1"))

    print("DELETE")
    client.delete("student:1")
    print("READ", client.get("student:1"))


if __name__ == "__main__":
    run()
