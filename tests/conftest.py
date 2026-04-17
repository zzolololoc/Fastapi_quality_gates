from typing import Any, Generator

import pytest
from flask import Flask

from app import create_app
from app import db as _db


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app("config.TestConfig")
    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app: Flask) -> Any:
    return app.test_client()


@pytest.fixture
def db(app: Flask) -> Any:
    return _db
