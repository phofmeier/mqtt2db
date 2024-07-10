import logging

from pymongo import MongoClient


class MongoDBImplementation:
    def __init__(self, config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.client = MongoClient(config["connection_string"])

        self.data_types = ["static", "timed"]

    def add(self, database: str, type: str, collection: str, data):
        self.client[database][collection].insert_one(data)

    def isTypeValid(self, name: str) -> bool:
        return name in self.data_types
