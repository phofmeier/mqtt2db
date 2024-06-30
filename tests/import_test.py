import pytest


def test_import():
    try:
        import mqtt2db.mqtt2db  # noqa: F401
    except ImportError:
        pytest.fail("Import Error occurred. Check dependencies.")
