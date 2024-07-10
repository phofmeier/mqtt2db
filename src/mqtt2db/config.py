import yaml


class Config:
    def __init__(self, filename: str) -> None:
        self._default_config = {
            "mqtt": {
                "broker": "localhost",
                "port": 1883,
                "channel_prefix": "data",
            },
            "database": {
                "connection_string": "localhost:27017",
            },
        }

        self._filename = filename
        try:
            with open(self._filename, "r") as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            self.config = self._default_config
            self.save()

    def save(self):
        with open(self._filename, "w") as file:
            yaml.dump(self.config, file)

    def get(self, name) -> dict:
        return self.config[name]
