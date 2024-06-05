from unittest.mock import MagicMock
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from backend.src.main import app, analyse_throw
from backend.src.helper import (CoinToss)
from random import choice

client = TestClient(app)

test_cases = [8, 10, 20]
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


@pytest.mark.parametrize("num_throws", test_cases)
def test_create_throws(mock_db_session, num_throws):
    request_data = throws(num_throws)
    response = client.post(f"{THROW_URL}/{num_throws}", json=request_data)
    assert response.status_code == 200
    assert response.json() == request_data

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


@pytest.mark.parametrize("num_throws", test_cases)
def test_create_throws_too_many_keys(mock_db_session, num_throws):
    request_data = throws(num_throws)
    request_data["scenario"] = 3  # adding invalid key with invalid value, should be ignored
    response = client.post(f"{THROW_URL}/{num_throws}", json=request_data)

    assert response.status_code == 200
    assert response.json() != request_data
    assert response.json() == {k: value for k, value in request_data.items() if k != "scenario"}

    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()


@pytest.mark.parametrize("num_throws", test_cases)
def test_create_throws_missing_throw(mock_db_session, num_throws):
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


@pytest.mark.parametrize("num_throws", test_cases)
def test_creat_throws_invalid_value(mock_db_session, num_throws):
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


@pytest.mark.parametrize("num_throws", test_cases)
def test_get_throws(mock_db_session, num_throws):
    test_data = create_dataframe(num_throws)
    df = pd.DataFrame(test_data)
    response = analyse_throw(df)
    assert isinstance(response, dict)

    # Check the Count functionality
    assert isinstance(response["count"]["heads"], dict)
    assert isinstance(response["count"]["tails"], dict)
    assert response["count"]["heads"].keys() == response["count"]["tails"].keys()
    for key, value in response["count"]["heads"].items():
        assert value + response["count"]["tails"][key] == response["total"]

    # Check the consecutive functionality
    assert isinstance(response["consecutive"]["mean"]["heads"], float)
    assert isinstance(response["consecutive"]["mean"]["tails"], float)
    assert isinstance(response["consecutive"]["std"]["heads"], float)
    assert isinstance(response["consecutive"]["std"]["tails"], float)
    assert isinstance(response["consecutive"]["percentages"]["heads"], dict)
    assert isinstance(response["consecutive"]["percentages"]["tails"], dict)
    assert isinstance(response["consecutive"]["data"]["heads"], dict)
    assert isinstance(response["consecutive"]["data"]["tails"], dict)


@pytest.mark.parametrize("num_throws", test_cases)
def test_get_throws_only_tails(mock_db_session, num_throws):
    # Create a dataframe with only heads
    test_data = create_dataframe(num_throws)
    df_tails = pd.DataFrame(test_data)
    df_tails[df_tails == "heads"] = "tails"
    response = analyse_throw(df_tails)

    # check the Count functionality
    for key, value in response["count"]["tails"].items():
        assert value == response["total"]

    # Check the consecutive functionality
    assert response["consecutive"]["mean"]["tails"] == num_throws
    assert response["consecutive"]["mean"]["heads"] == 0

    # Since all the throws are tails, the standard deviation should be 0
    assert response["consecutive"]["std"]["tails"] == 0
    assert response["consecutive"]["std"]["heads"] == 0

    # Since all the throws are tails, the max consecutive tails throw should be 100%
    assert response["consecutive"]["percentages"]["tails"][num_throws] == 100
    assert response["consecutive"]["data"]["tails"][num_throws] == 100


@pytest.mark.parametrize("num_throws", test_cases)
def test_get_throws_only_heads(mock_db_session, num_throws):
    # Create a dataframe with only heads
    test_data = create_dataframe(num_throws)
    df_heads = pd.DataFrame(test_data)
    df_heads[df_heads == "tails"] = "heads"
    response = analyse_throw(df_heads)

    # Check the Count functionality
    for key, value in response["count"]["heads"].items():
        assert value == response["total"]

    # Check the consecutive functionality
    assert response["consecutive"]["mean"]["tails"] == 0
    assert response["consecutive"]["mean"]["heads"] == num_throws

    assert response["consecutive"]["std"]["tails"] == 0
    assert response["consecutive"]["std"]["heads"] == 0

    assert response["consecutive"]["percentages"]["heads"][num_throws] == 100
    assert response["consecutive"]["data"]["heads"][num_throws] == 100


@pytest.mark.parametrize("num_throws", test_cases)
def test_get_throws_mixed_equal(mock_db_session, num_throws):
    # Create a dataframe with only heads
    test_data = create_dataframe(num_throws)

    df_heads = pd.DataFrame(test_data)
    df_heads[df_heads == "tails"] = "heads"

    df_tails = df_heads.copy()
    df_tails[df_tails == "heads"] = "tails"

    # concatenate df_tails with df_heads. The output should be 50% heads and 50% tails
    df_concat = pd.concat([df_tails, df_heads])
    response = analyse_throw(df_concat)

    # Check the Count functionality
    for key, value in response["count"]["tails"].items():
        assert value == response["total"] / 2

    # Check the consecutive functionality
    assert response["consecutive"]["mean"]["tails"] == num_throws / 2
    assert response["consecutive"]["mean"]["heads"] == num_throws / 2

    assert round(response["consecutive"]["std"]["tails"]) == num_throws / 2
    assert round(response["consecutive"]["std"]["heads"]) == num_throws / 2

    # Since we have 50% heads and 50% tails, the max consecutive tails should be 100% for each.
    assert response["consecutive"]["percentages"]["tails"][num_throws] == 50
    assert response["consecutive"]["data"]["tails"][num_throws] == 100

    assert response["consecutive"]["percentages"]["heads"][num_throws] == 50
    assert response["consecutive"]["data"]["heads"][num_throws] == 100
