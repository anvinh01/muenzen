import unittest.mock
import pytest
from backend.src.main import app, get_db
from dataclasses import dataclass

mock_session = unittest.mock.MagicMock()


def override_get_db():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def mock_db_session():
    mock_session.reset_mock()
    return mock_session


