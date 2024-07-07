import logging

from pymongo import MongoClient


class Database:
    def __init__(self, connection_string: str = "localhost:27017") -> None:
        self.logger = logging.getLogger(__name__)
        self.client = MongoClient(connection_string)
        self.database = self.client["mqtt_db"]

    def add(self, collection: str, data):
        self.database[collection].insert_one(data)
