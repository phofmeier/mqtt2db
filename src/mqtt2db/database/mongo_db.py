import logging

from pymongo import MongoClient


class MongoDBImplementation:
    def __init__(self, config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.client = MongoClient(config["connection_string"])

        self.data_types = ["static", "timed"]

    def addStaticData(self, database: str, collection: str, data):
        id_filed_name = self.config["static"]["id_field_name"]
        self.client[database][collection + "_static"].replace_one(
            {id_filed_name: data[id_filed_name]},
            data,
            upsert=True,
        )

    def addTimedData(self, database: str, collection: str, data):
        collection_name = collection + "_timed"
        if collection_name not in self.getCollectionNames(database):
            # Insert new collection
            self.client[database].create_collection(
                collection_name,
                timeseries={
                    "timeField": self.config["timed"]["time_field_name"],
                    "metaField": self.config["timed"]["meta_field_name"],
                },
            )
        self.client[database][collection + "_timed"].insert_one(data)

    def getDatabasesNames(self) -> list[str]:
        return self.client.list_database_names()

    def getCollectionNames(self, database_name: str) -> list[str]:
        return self.client[database_name].list_collection_names()

    def getAllDataFrom(self, database: str, collection: str):
        return list(self.client[database][collection].find({}, {"_id": False}))

    def getAllTimedDataFrom(self, database: str, collection: str):
        return list(self.client[database][collection].find({}, {}))
