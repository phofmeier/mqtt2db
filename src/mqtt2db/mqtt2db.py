import logging
import logging.config

from mqtt2db.config import Config
from mqtt2db.database.database import Database
from mqtt2db.mqtt import MQTTConnection


def init_logger(logging_config: dict):
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    return logger


def main():
    """Initialize and run the Application"""
    config = Config("config.yml")
    logger = init_logger(config.get("logging"))
    database = Database(config.get("database"))
    mqtt = MQTTConnection(database, config.get("mqtt"))
    logger.info("Run application.")
    mqtt.run()


if __name__ == "__main__":
    main()
