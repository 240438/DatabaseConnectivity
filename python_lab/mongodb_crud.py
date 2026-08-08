from pymongo import MongoClient

from config_loader import get_setting


def run() -> None:
    username = get_setting("mongodb", "username", "MONGODB_USERNAME")
    secret = get_setting("mongodb", "secret", "MONGODB_SECRET")
    host = get_setting("mongodb", "host", "MONGODB_HOST")
    port = get_setting("mongodb", "port", "MONGODB_PORT")
    auth_source = get_setting("mongodb", "auth_source", "MONGODB_AUTH_SOURCE")

    if username:
        uri = f"mongodb://{username}:{secret}@{host}:{port}/?authSource={auth_source}"
    else:
        uri = f"mongodb://{host}:{port}/"

    client = MongoClient(uri)
    db = client[get_setting("mongodb", "database", "MONGODB_DATABASE")]
    collection = db.students

    print("CREATE")
    collection.insert_one({"_id": 1, "name": "Asha", "course": "DB"})

    print("READ", collection.find_one({"_id": 1}))

    print("UPDATE")
    collection.update_one({"_id": 1}, {"$set": {"course": "Advanced DB"}})
    print("READ", collection.find_one({"_id": 1}))

    print("DELETE")
    collection.delete_one({"_id": 1})
    print("READ", collection.find_one({"_id": 1}))


if __name__ == "__main__":
    run()
