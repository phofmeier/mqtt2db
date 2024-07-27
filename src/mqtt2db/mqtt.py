import json
import logging

import paho.mqtt.client as mqtt

from mqtt2db.database.database import Database


class MQTTConnection:
    """Class to manage the connection to the MQTT broker."""

    def __init__(self, database: Database, config: dict) -> None:
        """Initialize the Connection to the MQTT broker.

        Args:
            database (Database): Database interface where the incoming data is stored.
            config (dict): MQTT configuration.
        """
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

        self.logger.debug(f"Connect to mqtt client with config: {self.config}")
        self.mqttc.connect(self.config["broker"], self.config["port"])

    def run(self):
        """Run the mqtt client in an endless loop."""
        self.mqttc.loop_forever()
