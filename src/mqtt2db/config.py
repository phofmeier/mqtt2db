import logging

import yaml


class Config:
    """Class for providing and manage the configuration."""

    def __init__(self, filename: str) -> None:
        self._default_config = {
            "mqtt": {
                "broker": "localhost",
                "port": 1883,
                "channel_prefix": "data",
            },
            "database": {
                "connection_string": "localhost:27017",
                "static": {
                    "id_field_name": "id",
                },
                "timed": {
                    "time_field_name": "timestamp",
                    "meta_field_name": "metadata",
                },
            },
            "logging": {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "f": {
                        "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
                    }
                },
                "handlers": {
                    "h": {
                        "class": "logging.StreamHandler",
                        "formatter": "f",
                        "level": logging.INFO,
                    }
                },
                "root": {
                    "handlers": ["h"],
                    "level": logging.INFO,
                },
            },
        }

        self._filename = filename
        try:
            with open(self._filename, "r") as file:
                self.config = yaml.safe_load(file)
                self.config = Config.deepMergeDict(self.config, self._default_config)
        except FileNotFoundError:
            self.config = self._default_config

        self.save()

    def save(self):
        """Save the current configuration to the disc."""
        with open(self._filename, "w") as file:
            yaml.dump(self.config, file)

    def get(self, name: str) -> dict:
        """Get the configuration of a specific component.

        Args:
            name (str): Name of the part of the config

        Returns:
            dict: All configuration data
        """
        return self.config[name]

    @staticmethod
    def deepMergeDict(source: dict, destination: dict) -> dict:
        """Deep merge two dictionaries.

        Args:
            source (dict): dict from where we get the values.
            destination (dict): where to put or replace the values from source.

        Returns:
            dict: new dictionary containing the merged values.
        """
        for key, value in source.items():
            if isinstance(value, dict):
                # get node or create one
                node = destination.setdefault(key, {})
                Config.deepMergeDict(value, node)
            else:
                destination[key] = value

        return destination
