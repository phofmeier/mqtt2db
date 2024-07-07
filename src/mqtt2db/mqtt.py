import json
import logging

import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883


class MQTTConnection:
    def __init__(self, database) -> None:
        self.logger = logging.getLogger(__name__)

        def on_connect(client, userdata, flags, reason_code, properties):
            self.logger.info(f"Connected with result code {reason_code}")
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe("data/#")

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, msg):
            # print(
            #     "On:"
            #     + msg.topic
            #     + " Receivied: "
            #     + str(msg.payload)
            #     + " Userdata:"
            #     + str(userdata)
            # )
            collection = "_".join(msg.topic.split("/")[1:])
            data = json.loads(msg.payload)

            self.logger.debug(
                f"Received data on collection {collection} with data: {data}"
            )
            database.add(collection, data)

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message

        self.mqttc.connect(broker, port, 60)

    def run(self):
        self.mqttc.loop_forever()
