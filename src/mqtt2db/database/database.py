import logging

from mqtt2db.database.mongo_db import MongoDBImplementation


class Database:
    def __init__(self, config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.database_impl = MongoDBImplementation(config)

        self.data_types = ["static", "timed"]

    def add(self, database: str, type: str, collection: str, data):
        self.database_impl.add(database, type, collection, data)

    def isTypeValid(self, name: str) -> bool:
        return name in self.data_types

    def getDatabasesNames(self) -> list[str]:
        return self.database_impl.getDatabasesNames()

    def getCollectionNames(self, database_name: str) -> list[str]:
        return self.database_impl.getCollectionNames(database_name)

    def getAllDataFrom(self, database: str, collection: str):
        return self.database_impl.getAllDataFrom(database, collection)
