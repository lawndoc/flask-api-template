from api import app
import pytest


@pytest.fixture
def client():
    app.config["LOG_LEVEL"] = 5
    app.testing = True
    yield app.test_client()