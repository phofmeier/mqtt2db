import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.connect(broker, port, 60)
