import unittest.mock
import pytest
from src.main import app, get_db

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


@pytest.fixture()
def test_cases():
    return [8, 10, 20]
