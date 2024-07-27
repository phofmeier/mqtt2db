[![pre-commit](https://github.com/phofmeier/mqtt2db/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/phofmeier/mqtt2db/actions/workflows/pre-commit.yml)
[![Unit Tests](https://github.com/phofmeier/mqtt2db/actions/workflows/unittests.yml/badge.svg)](https://github.com/phofmeier/mqtt2db/actions/workflows/unittests.yml)
[![Dependabot Updates](https://github.com/phofmeier/mqtt2db/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/phofmeier/mqtt2db/actions/workflows/dependabot/dependabot-updates)

# MQTT2DB

## Overview

This application subscribes to channels on mqtt broker and adds the data to MongoDB database.

## Deployment

### Local installation

Install and run the application locally using pip.

```sh
python3.11 -m venv ./venv/
source venv/bin/activate
pip install . # or use pip install -e .[dev] for development
mqtt2db
```

### Docker

Checkout the example for using this app with docker compose [here](example/README.md).

Or only run the app in a container with the following command.

```sh
docker run -d -p1883:1883 -p27017:27017 -v ./config.yml:/home/app/config.yml ghcr.io/phofmeier/mqtt2db:latest
```

## Architecture

### Channel scheme

`<prefix>/<database>/<type>/<collection>`

- Prefix: All data send to this prefix are taken into account
- Database: Name of the Database where the data is saved
- Type: of the Data `static` or `timed` see [Data Formats](#data-formats) for more information
- Collection: A collection holds data of the same type

### Database

The connection to a database is implemented as an Interface such that different database types can be used.

Currently supported databases:

- MongoDB

### Data Formats

All data needs to be in a json format.

#### Static

Static data which does not change during time. All data requires a unique id field configurable via the `<id_field_name>` entry. New data with the same `<id_field_name>` replace the old data with the new one.

#### Timed

All data has a timestamped and is sorted in a time based manner.
Each data needs an entry with the key `<timefield>` including the timestamp. The timestamp needs to be present in ISO 8601 format. Additionally there is optional meta data on the `<meta_field_name>` key.

## Tools

This application ships with two small tools for testing purpose

### mqtt2db_dash

A small plotly dash app to show the data inside the database. run `mqtt2db_dash` to start the app.

### Publish data script

The script [publish_mqtt.py](tools/publish_mqtt.py) can be used to publish some test data to the application.
