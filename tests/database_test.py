from mqtt2db.config import Config
from mqtt2db.database.database import Database


def test_database():
    config = Config("config.yml")
    db = Database(config.get("database"))
    assert db.isTypeValid("timed")
    assert db.isTypeValid("static")
    assert not db.isTypeValid("other")
    assert not db.isTypeValid("")
