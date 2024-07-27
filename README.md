![Pre Commit](https://github.com/phofmeier/mqtt2db/actions/workflows/pre-commit.yml/badge.svg)
![Unit Tests](https://github.com/phofmeier/mqtt2db/actions/workflows/unittests.yml/badge.svg)
[![Dependabot Updates](https://github.com/phofmeier/mqtt2db/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/phofmeier/mqtt2db/actions/workflows/dependabot/dependabot-updates)

# MQTT2DB

## Overview

This application subscribes to channels on mqtt broker and adds the data to MongoDB database.

## Deployment

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

Static data which does not change during time. All data requires a id filed. New data with the same `<id_field_name>` replace the old data with the new one.

#### Timed

All data has a timestamped and is sorted in a time based manner.
Each data needs an entry with the key `<timefield>` including the timestamp. The timestamp needs to be present in ISO 8601 format. Additionally there is optional meta data on the `<meta_field_name>` key.
