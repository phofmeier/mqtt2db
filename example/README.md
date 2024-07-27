# Example usage with Docker Compose

This example contains a docker compose configuration launching 3 container.

- 1. The MQTT2DB application
- 2. The Mosquitto MQTT broker
- 3. A MongoDB Database

There is no authentication used anywhere. So please do not use this example for production. 


## Instruction for testing

### Run Docker container with docker compose
```
cd ./example
docker compose build
docker compose up
```

### Install locally
```
python3.11 -m venv ./venv 
source venv/bin/activate 
pip install .
``` 

### Publish data to database

```
python3.11 tools/publish_mqtt.py
```

### Show data in app
```
mqtt2db_dash
```

