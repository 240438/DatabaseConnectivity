from elasticsearch import Elasticsearch

from config_loader import get_setting


def run() -> None:
    host = get_setting("elasticsearch", "host", "ELASTICSEARCH_HOST")
    username = get_setting("elasticsearch", "username", "ELASTICSEARCH_USERNAME")
    secret = get_setting("elasticsearch", "secret", "ELASTICSEARCH_SECRET")
    index = get_setting("elasticsearch", "index", "ELASTICSEARCH_INDEX")

    auth = (username, secret) if username else None
    client = Elasticsearch(hosts=[host], basic_auth=auth)

    print("CREATE")
    client.index(index=index, id=1, document={"name": "Asha", "course": "DB"}, refresh=True)

    print("READ", client.get(index=index, id=1)["_source"])

    print("UPDATE")
    client.update(index=index, id=1, doc={"course": "Advanced DB"}, refresh=True)
    print("READ", client.get(index=index, id=1)["_source"])

    print("DELETE")
    client.delete(index=index, id=1, refresh=True)
    print(client.exists(index=index, id=1))


if __name__ == "__main__":
    run()
