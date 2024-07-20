import datetime
import json

import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(broker, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
test_item = {
    "id": "TestUniqueid2",
    "item_name": "test_3",
    "item_val": 10.1,
    "another_thing": "as String",
}

test_item_json = json.dumps(test_item)


mqttc.publish("data/test_db/static/node", test_item_json)
mqttc.publish("test_2/test_node_1", "testMessage")

timed_item = {
    "timestamp": datetime.datetime.now().isoformat(),
    "temperature": 10.9,
    "humidity": 35.4,
}

timed_item_json = json.dumps(timed_item)

mqttc.publish("data/test_db/timed/temperature", timed_item_json)

mqttc.loop_forever()
