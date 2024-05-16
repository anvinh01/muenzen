from unittest.mock import MagicMock

import pandas as pd
from fastapi.testclient import TestClient

from src.main import app, analyse_throw
from src.helper import CoinToss
from random import choice

client = TestClient(app)

THROW_URL = "/throws"
coin = [CoinToss.heads.value, CoinToss.tails.value]


def throws(num_throws=8) -> dict:
    request_throw = {}

    for i in range(1, num_throws + 1):
        request_throw[f"throw_{str(i)}"] = choice(coin)

    return request_throw


def create_dataframe(num_throws: int) -> pd.DataFrame:
    num_rows = 100
    return pd.DataFrame(
        {"id" if k == 0 else k: [choice(coin) for _ in range(num_rows)]
         for k in range(0, num_throws + 1)}
    )


def post_throws(mock_db_session: MagicMock, num_throws=8):
    request_data = throws(num_throws)
    response = client.post(f"{THROW_URL}/{num_throws}", json=request_data)
    assert response.status_code == 200
    assert response.json() == request_data

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

    return response.json()


def test_create_throws(mock_db_session, test_cases):
    for num_throws in test_cases:
        post_throws(mock_db_session, num_throws)


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


def test_get_throws(mock_db_session, test_cases):
    for num_throws in test_cases:
        test_data = create_dataframe(num_throws)
        df = pd.DataFrame(test_data)
        response = analyse_throw(df)
        assert isinstance(response, dict)
        assert (response["mean_heads"] + response["mean_tails"] == 100).all()

        # extend the dataframe with the flipped version of the original dataframe
        df_tails = df.copy()
        df_tails[df_tails == "heads"] = "tails"
        response = analyse_throw(df_tails)
        assert (response["mean_heads"] == 0).all()
        assert (response["mean_tails"] == 100).all()

        df_heads = df_tails.copy()
        df_heads[df_heads == "tails"] = "heads"
        response = analyse_throw(df_heads)
        assert (response["mean_heads"] == 100).all()
        assert (response["mean_tails"] == 0).all()

        # concatenate df_tails with df_heads. The output should be 50% heads and 50% tails
        df_concat = pd.concat([df_tails, df_heads])
        response = analyse_throw(df_concat)
        assert (response["mean_heads"] == 50).all()
        assert (response["mean_tails"] == 50).all()
