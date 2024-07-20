import datetime
import logging
from typing import Optional

from mqtt2db.database.mongo_db import MongoDBImplementation


class Database:
    def __init__(self, config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.database_impl = MongoDBImplementation(config)

        self.data_types = ["static", "timed"]

    def add(self, database: str, type: str, collection: str, data: dict):
        if type not in self.data_types:
            self.logger.error(
                f"Cannot add data of type: {type} to database."
                f"Allowed types are: {self.data_types}"
            )
            return
        if type == "static":
            self.database_impl.addStaticData(database, collection, data)
            return
        if type == "timed":
            if self.verifyTimedData(data):
                self.database_impl.addTimedData(database, collection, data)
            return

    def isTypeValid(self, name: str) -> bool:
        return name in self.data_types

    def verifyStaticData(self, data: dict) -> bool:
        id_filed_name = self.config["static"]["id_field_name"]
        if id_filed_name not in data.keys():
            self.logger.warning(
                f"Static value data does not contain the required"
                f"key {id_filed_name} The received data is: {data}"
            )
            return False
        return True

    def verifyTimedData(self, data: dict) -> bool:
        time_field_name = self.config["timed"]["time_field_name"]
        if time_field_name not in data.keys():
            self.logger.warning(
                f"Timed value data does not contain the required"
                f"key {time_field_name} The received data is: {data}"
            )
            return False
        try:
            datetime_ts = datetime.datetime.fromisoformat(data[time_field_name])
        except ValueError:
            self.logger.warning(
                f"Timed value timestamp is not presented as an ISO 8601 format "
                f"and con not be converted. Received value: {data[time_field_name]}"
            )
            return False

        data[time_field_name] = datetime_ts

        return True

    def getDatabasesNames(self) -> list[str]:
        return self.database_impl.getDatabasesNames()

    def getCollectionNames(
        self, database_name: str, type: Optional[str] = None
    ) -> list[str]:
        if type is None or not self.isTypeValid(type):
            return self.database_impl.getCollectionNames(database_name)
        return [
            col
            for col in self.database_impl.getCollectionNames(database_name)
            if col.endswith(type) and not col.startswith("system.")
        ]

    def getAllDataFrom(self, database: str, collection: str):
        return self.database_impl.getAllDataFrom(database, collection)

    def getAllTimedDataFrom(self, database: str, collection: str):
        return self.database_impl.getAllTimedDataFrom(database, collection)
