import json
import logging

import paho.mqtt.client as mqtt

from mqtt2db.database.database import Database


class MQTTConnection:
    def __init__(self, database: Database, config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.prefix = self.config["channel_prefix"].strip("/")
        self.database = database

        def on_connect(client, userdata, flags, reason_code, properties):
            self.logger.info(f"Connected with result code {reason_code}")
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe(self.prefix + "/#")

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            channel = msg.topic[len(self.prefix) + 1 :].split("/")
            if len(channel) < 3:
                self.logger.warning(
                    f"Message arrived on wrong formatted channel: {channel}."
                )
                return
            database_name = channel[0]
            type_name = channel[1]
            if not self.database.isTypeValid(type_name):
                self.logger.warning(f"Message arrived with invalid type: {type_name}.")
                return

            collection = "_".join(channel[2:])

            data = json.loads(msg.payload)

            self.logger.debug(
                f"Received data for database: {database_name} as type: {type_name} "
                f"for collection: {collection} with data: {data}"
            )
            self.database.add(database_name, type_name, collection, data)

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message

        self.mqttc.connect(self.config["broker"], self.config["port"])

    def run(self):
        self.mqttc.loop_forever()
