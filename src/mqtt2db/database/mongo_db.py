import logging

from pymongo import MongoClient


class MongoDBImplementation:
    def __init__(self, config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.client = MongoClient(config["connection_string"])

        self.data_types = ["static", "timed"]

    def add(self, database: str, type: str, collection: str, data):
        self.client[database][collection].insert_one(data)

    def getDatabasesNames(self) -> list[str]:
        return self.client.list_database_names()

    def getCollectionNames(self, database_name: str) -> list[str]:
        return self.client[database_name].list_collection_names()

    def getAllDataFrom(self, database: str, collection: str):
        return list(self.client[database][collection].find({}, {"_id": False}))
