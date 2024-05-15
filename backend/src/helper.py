import enum
from pydantic import BaseModel, create_model, Field, field_validator
from sqlalchemy import Column, Integer, Enum

# !!!!!!! Don't remove Session from sqlalchemy.orm. It is used by fastapi, even if Pycharm doesn't recognize it
# noinspection PyUnresolvedReferences
from sqlalchemy.orm import Session, declarative_base


class CoinToss(enum.Enum):
    heads = "heads"
    tails = "tails"


def create_throw_class(num_throws, base: declarative_base):
    attrs = {
        "__tablename__": f"toss_{num_throws}",
        "id": Column(Integer, primary_key=True)
    }

    for i in range(1, num_throws + 1):
        attrs[f"throw_{i}"] = Column(Enum(CoinToss), nullable=False)

    return type(f"Throw{num_throws}", (base,), attrs)


class ThrowBase(BaseModel):

    # noinspection PyMethodParameters
    @field_validator('*')  # <-- Apply validator to all fields in subclasses of ThrowBase
    def validate_value(v):
        ALLOWED_VALUES = ['heads', 'tails']
        if v not in ALLOWED_VALUES:
            raise ValueError(f'Unexpected value {v}, allowed values are {ALLOWED_VALUES}')
        return v


def create_throw_class_crud(n: int):
    # Create a dictionary to store your fields
    fields = {f'throw_{i + 1}': (str, Field(...)) for i in range(n)}

    # Create new model_type class by using `create_model`
    # It accepts class name as first parameter, and then unpack your fields dictionary
    return create_model(f'ThrowCreate{n}', **fields, __base__=ThrowBase)
