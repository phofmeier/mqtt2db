from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client["test_db"]


if __name__ == "__main__":

    dbname = get_database()
    collection = dbname["test_collection"]

    test_item = {
        "_id": "001",
        "item_name": "test_1",
        "item_val": 10.1,
    }
    collection.insert_one(test_item)

    print(collection.find_one())
