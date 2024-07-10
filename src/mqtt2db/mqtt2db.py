import logging
import logging.config

from mqtt2db.config import Config
from mqtt2db.database.database import Database
from mqtt2db.mqtt import MQTTConnection


def init_logger():
    logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            "f": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"}
        },
        handlers={
            "h": {
                "class": "logging.StreamHandler",
                "formatter": "f",
                "level": logging.DEBUG,
            }
        },
        root={
            "handlers": ["h"],
            "level": logging.DEBUG,
        },
    )
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    return logger


def main():
    config = Config("config.yml")
    logger = init_logger()
    database = Database(config.get("database"))
    mqtt = MQTTConnection(database, config.get("mqtt"))
    logger.info("Run application.")
    mqtt.run()


if __name__ == "__main__":
    main()
