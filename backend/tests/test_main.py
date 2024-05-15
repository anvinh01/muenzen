from fastapi.testclient import TestClient

from src.main import app
from src.helper import CoinToss
from random import choice

client = TestClient(app)

THROW_URL = "/throws"


def throws(num_throws=8) -> dict:
    coin = [CoinToss.heads.value, CoinToss.tails.value]
    request_throw = {}

    for i in range(1, num_throws + 1):
        request_throw[f"throw_{str(i)}"] = choice(coin)

    return request_throw


def test_create_throws(mock_db_session, test_cases):
    for num_throws in test_cases:
        request_data = throws(num_throws)
        response = client.post(f"{THROW_URL}/{num_throws}", json=request_data)
        assert response.status_code == 200
        assert response.json() == request_data

        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called()


def test_create_throws_too_many_keys(mock_db_session, test_cases):
    for num_throws in test_cases:
        request_data = throws(num_throws)
        request_data["scenario"] = 3  # adding invalid key with invalid value, should be ignored
        response = client.post(f"{THROW_URL}/{num_throws}", json=request_data)

        assert response.status_code == 200
        assert response.json() != request_data
        assert response.json() == {k: value for k, value in request_data.items() if k != "scenario"}

        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called()


def test_create_throws_missing_throw(mock_db_session, test_cases):
    for num_throws in test_cases:
        # Creating a request_data with invalid throw order
        # The throw order will skip the number 8 and instead be number 9
        # The Test should ignore the number 9, but should notice that the 8 is missing
        request_data = throws(num_throws)
        request_data["throw_9"] = request_data["throw_8"]
        del request_data["throw_8"]
        response = client.post(f"{THROW_URL}/{num_throws}", json=request_data)
        assert response.status_code == 422
        assert response.json() == dict(
            detail=[{'input': request_data, 'loc': ['body', 'throw_8'], 'msg': 'Field required', 'type': 'missing'}])

        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()


def test_creat_throws_invalid_value(mock_db_session, test_cases):
    for num_throws in test_cases:
        # Creating request_data with invalid spelling of heads
        request_data = throws(num_throws)
        request_data["throw_1"] = "head"  # Invalid spelling of heads
        response = client.post(f"{THROW_URL}/{num_throws}", json=request_data)
        assert response.status_code == 422
        assert response.json() == dict(detail=[{'ctx': {'error': {}}, 'input': 'head', 'loc': ['body', 'throw_1'],
                                                'msg': 'Value error, Unexpected value head, allowed values are '
                                                       "['heads', 'tails']", 'type': 'value_error'}])
        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()
