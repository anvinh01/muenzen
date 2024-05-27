import enum
from itertools import groupby
import pandas as pd
from pydantic import BaseModel, create_model, Field, field_validator
from sqlalchemy import Column, Integer, Enum

# !!!!!!! Don't remove Session from sqlalchemy.orm. It is used by fastapi, even if Pycharm doesn't recognize it
# noinspection PyUnresolvedReferences
from sqlalchemy.orm import Session, declarative_base

'''
These are helper functions, which are used to create the models and the API-Endpoints.
'''


# Create an enum for the CoinToss, since the CoinToss can only be heads or tails.
class CoinToss(enum.Enum):
    heads = "heads"
    tails = "tails"


def create_throw_class(num_throws: int, base: declarative_base):
    """
    :type base: declarative_base
    :type num_throws: int

    This function creates a new class, which inherits from the base class.
    The name of the new class will be Throw<num_throws>, where <num_throws> is the number of throws.
    The new class will have <num_throws> columns, where each column represents a throw.
    The name of each column will be throw_<num_throws>, where <num_throws> is the number of throws.
    The type of each column will be Enum(CoinToss), where CoinToss is the enum
    The __tablename__ of the new class will be toss_<num_throws>
    """

    # Create a dictionary to store your fields
    attrs = {
        "__tablename__": f"toss_{num_throws}",
        "id": Column(Integer, primary_key=True)
    }

    # Add the columns to the dictionary, where the key is the name of the column and the value is the column itself
    for i in range(1, num_throws + 1):
        attrs[f"throw_{i}"] = Column(Enum(CoinToss), nullable=False)

    # Create new model_type class by using `create_model`
    return type(f"Throw{num_throws}", (base,), attrs)


class ThrowBase(BaseModel):
    """
    This is the base class for all the Throw classes.
    It has a field called id, which is the primary key of the table.
    It also validates the value of each column, before it is saved to the database.
    """

    # noinspection PyMethodParameters
    @field_validator('*')  # <-- Apply validator to all fields in subclasses of ThrowBase
    def validate_value(v):
        ALLOWED_VALUES = ['heads', 'tails']
        if v not in ALLOWED_VALUES:
            raise ValueError(f'Unexpected value {v}, allowed values are {ALLOWED_VALUES}')
        return v


def create_throw_class_crud(n: int):
    """
    :param n: int
    :return: ThrowCreate<n>

    This function creates a new class, which inherits from the ThrowBase class.
    The name of the new class will be ThrowCreate<num_throws>, where <num_throws> is the number of throws.
    The new class will have <num_throws> columns, where each column represents a throw.
    The name of each column will be throw_<num_throws>, where <num_throws> is the number of throws.
    The type of each column will be Enum(CoinToss), where CoinToss is the enum

    It will allow the user to create a POST request.
    Example:
    {
        "throw_1": "heads",
        "throw_2": "tails",
        "throw_3": "heads",
        "throw_4": "tails",
        ...,
    }
    """
    # Create a dictionary to store your fields
    fields = {f'throw_{i + 1}': (str, Field(...)) for i in range(n)}

    # Create new model_type class by using `create_model`
    # It accepts class name as first parameter, and then unpack your fields dictionary
    return create_model(f'ThrowCreate{n}', **fields, __base__=ThrowBase)


# ===================================[ Dataframes functions ]==================================
def len_iter(items):
    return sum(1 for _ in items)


def consecutive_helper(data, bin_val):
    return max((len_iter(run) for val, run in groupby(data) if val == bin_val), default=0)


def consecutive_values(df: pd.DataFrame) -> tuple[list, list]:

    consecutive_heads = df.apply(consecutive_helper, bin_val="heads", axis=1)
    consecutive_tails = df.apply(consecutive_helper, bin_val="tails", axis=1)

    consecutive_tails_mean = consecutive_tails.mean()
    consecutive_heads_mean = consecutive_heads.mean()

    consecutive_heads_std = consecutive_heads.std()
    consecutive_tails_std = consecutive_tails.std()

    consecutive_heads_number = (consecutive_heads.value_counts() * 100 // consecutive_heads.count()).to_dict()
    consecutive_heads_number = {number: consecutive_heads_number[number] if number in consecutive_heads_number else 0
                                for number in
                                range(1, len(df.keys()) + 1)}

    print(f"{consecutive_heads.count()}: consecutive: heads", consecutive_heads_number)

    '''
    print("consecutive: heads", consecutive_heads_mean)
    print("consecutive: heads std", consecutive_heads_std)
    print("consecutive: heads number", consecutive_heads_number)
    '''

    return consecutive_heads, consecutive_tails
