from fastapi.testclient import TestClient
from .main import app, CoinToss
from random import choice
import json
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def throws(num_throws=8) -> dict:
    coin = [CoinToss.heads.value, CoinToss.tails.value]
    request_throw = {"scenario": num_throws, "selection": {}}

    for i in range(1, num_throws + 1):
        request_throw["selection"][str(i)] = choice(coin)

    return request_throw


def test_create_throws():
    request_data = throws(8)
    response = client.post("/throws/", json=request_data)
    assert response.status_code == 200
    assert response.json() == request_data


def test_create_throws_length_not_matching_scenario():
    request_data = throws(8)
    request_data["scenario"] = 3            # Scenario length has been changed to 3 and selection length is 8
    response = client.post("/throws/", json=request_data)
    assert response.status_code == 422
    assert response.json() == dict(detail=[
        {
            "type": "value_error",
            "loc": [
                "body"
            ],
            "msg": "Value error, Scenario and length of selection must be equal",
            "input": request_data,
            "ctx": {
                "error": {}
            }
        }
    ])


def test_create_throws_invalid_throw_order():
    # Creating a request_data with invalid throw order
    # The throw order will skip the number 8 and instead be number 9
    request_data = throws(8)
    request_data["selection"]["9"] = request_data["selection"]["8"]
    del request_data["selection"]["8"]
    response = client.post("/throws/", json=request_data)
    assert response.status_code == 422
    assert response.json() == dict(detail=[
        {
            "type": "value_error",
            "loc": [
                "body"
            ],
            "msg": "Value error, Keys of selection must be in ascending order",
            "input": request_data,
            "ctx": {
                "error": {}
            }
        }
    ])


def test_create_throws_invalid_scenario():
    # Creating request_data with scenario not in (9, 10, 20)
    request_data = throws(3)
    request_data["scenario"] = 3
    response = client.post("/throws/", json=request_data)
    assert response.status_code == 422
    assert response.json() == dict(detail=[
        {
            "type": "value_error",
            "loc": [
                "body"
            ],
            "msg": "Value error, selection must be of length 8, 10, or 20",
            "input": request_data,
            "ctx": {
                "error": {}
            }
        }
    ])


def test_creat_throws_invalid_spelling():
    # Creating request_data with invalid spelling of heads
    request_data = throws(8)
    request_data["selection"]["1"] = "head"
    response = client.post("/throws/", json=request_data)
    assert response.status_code == 422
    assert response.json() == dict(detail=[
        {
            "type": "enum",
            "loc": [
                "body",
                "selection",
                "1"
            ],
            "msg": "Input should be 'heads' or 'tails'",
            "input": "head",
            "ctx": {
                "expected": "'heads' or 'tails'"
            }
        }
    ])




