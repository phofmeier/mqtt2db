![Pre Commit](https://github.com/phofmeier/mqtt2db/actions/workflows/pre-commit.yml/badge.svg)
![Unit Tests](https://github.com/phofmeier/mqtt2db/actions/workflows/unittests.yml/badge.svg)

# MQTT2DB

## Overview

This application subscribes to channels on mqtt broker and adds the data to MongoDB database.

## Deployment

## Architecture

### Channel scheme

`<prefix>/<database>/<type>/<collection>`

- Prefix: All data send to this prefix are taken into account
- Database: Name of the Database where the data is saved
- Type: of the Data `static` or `timed` see !data_types
- Collection: A collection holds data of the same type

#### Database

### Data Types

- static: Static data which does not change. New data overwrites the old one depending on TBD
- timed: All data has a timestamped and is sorted in a time based manner
