import logging
import logging.config

from mqtt2db.database import Database
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
    logger = init_logger()
    database = Database()
    mqtt = MQTTConnection(database)
    logger.info("Run application.")
    mqtt.run()


if __name__ == "__main__":
    main()
