from fastapi import FastAPI
from typing import Dict
from typing_extensions import Self
from pydantic import BaseModel, model_validator
from fastapi.testclient import TestClient
from enum import Enum

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


class CoinToss(str, Enum):
    heads = "heads"
    tails = "tails"


class Throws(BaseModel):
    scenario: int
    selection: Dict[int, CoinToss]

    # Validating the input data.
    @model_validator(mode="after")
    def check_selection_length(self) -> Self:
        length = len(self.selection.values())

        # Check that the length of the selection is equal to the scenario.
        if length != self.scenario:
            raise ValueError("Scenario and length of selection must be equal")

        # Check that the length is 8, 10 or 20.
        if length not in (8, 10, 20):
            raise ValueError('selection must be of length 8, 10, or 20')

        # Check if the Keys of the selection are in ascending order.
        keys = list(self.selection.keys())
        keys.sort()
        if not (length in (8, 10, 20) and keys[0] == 1 and keys[-1] == length):
            raise ValueError('Keys of selection must be in ascending order')

        # OK
        return self


@app.post("/throws/")
async def create_throws(throws_data: Throws):  # throws_data is an instance of Throws
    # Your function's code here. For example:
    return {"scenario": throws_data.scenario, "selection": throws_data.selection}
