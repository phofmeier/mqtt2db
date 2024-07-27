import datetime
import json
from time import sleep

import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
published_messages = []

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect(broker, port, 60)
mqtt_client.loop_start()

test_item_static = {
    "id": "TestUniqueid3",
    "item_name": "test_3",
    "item_val": 10.1,
    "another_thing": "as String",
}

published_messages.append(
    mqtt_client.publish("data/test_db/static/node", json.dumps(test_item_static))
)
published_messages.append(mqtt_client.publish("test_2/test_node_1", "testMessage"))

timed_item = {
    "timestamp": datetime.datetime.now().isoformat(),
    "temperature": 10.9,
    "humidity": 35.4,
}


published_messages.append(
    mqtt_client.publish("data/test_db/timed/temperature", json.dumps(timed_item))
)

# Wait for publish everything before leaving
while mqtt_client.want_write() or any(
    [not msg.is_published() for msg in published_messages]
):
    sleep(1)
mqtt_client.loop_stop()
mqtt_client.disconnect()
