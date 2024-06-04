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

def count(df: pd.DataFrame) -> dict:
    """

    :param df: pd.DataFrame
    :return: dict
    preview:
    {
        heads : {throw_0: int, throw_1: int,...},
        tails : {throw_0: int, throw_1: int,...},
    }

    This Function counts the number of heads and tails in the dataframe.
    """

    # Count the number of heads and tails in the dataframe
    count_heads = df.apply(lambda x: (x == 'heads').sum())
    count_tails = df.apply(lambda x: (x == 'tails').sum())

    return dict(heads=count_heads.to_dict(), tails=count_tails.to_dict())


def len_iter(items):
    return sum(1 for _ in items)


def consecutive_helper(data, bin_val):
    return max((len_iter(run) for val, run in groupby(data) if val == bin_val), default=0)


def consecutive_values(df: pd.DataFrame) -> dict:
    """

    :param: df: pd.DataFrame
    :return: dict
    preview:
    {
        mean : {
            heads=consecutive_heads_mean,
            tails=consecutive_tails_mean,
        },
        std : {
            heads=consecutive_heads_std,
            tails=consecutive_tails_std,
        },
        percentages : {
            heads : {0: percentage, 1: percentage,...},
            tails : {0: percentage, 1: percentage,...},
        },
        data : {
            heads : {0: int, 1: int,...},
            tails : {0: int, 1: int,...},
        }
    }

    This function calculates the mean and the standard deviation of the consecutive heads and tails for each throw.
    First we get the max consecutive heads and tails for each throw round.
    Then we calculate the mean and stadard deviation of the consecutive heads and tails.

    We also count the number of max consecutive heads and tails and return it once in percentages and int.
    """

    # Calculate the number of max consecutive heads and tails for each throw
    consecutive_heads = df.apply(consecutive_helper, bin_val="heads", axis=1)
    consecutive_tails = df.apply(consecutive_helper, bin_val="tails", axis=1)

    # Calculate the mean of the consecutive heads and tails
    consecutive_tails_mean = consecutive_tails.mean()
    consecutive_heads_mean = consecutive_heads.mean()

    # Calculate the standard deviation of the consecutive heads and tails
    consecutive_heads_std = consecutive_heads.std()
    consecutive_tails_std = consecutive_tails.std()

    # Count the number of max consecutive heads in percentages
    consecutive_heads_percentages = (round(consecutive_heads.value_counts() * 100 / consecutive_heads.count(), 2)
                                     .to_dict())
    consecutive_heads_data_percentage = {
        number: consecutive_heads_percentages[number] if number in consecutive_heads_percentages else 0
        for number in range(0, len(df.keys()) + 1)
    }

    # Count the number of max consecutive heads
    consecutive_heads_count = consecutive_heads.value_counts().to_dict()
    consecutive_heads_data = {
        number: consecutive_heads_count[number] if number in consecutive_heads_count else 0
        for number in range(0, len(df.keys()) + 1)
    }

    # Count the number of max consecutive tails in percentages
    consecutive_tails_percentages = (round(consecutive_tails.value_counts() * 100 / consecutive_tails.count(), 2)
                                     .to_dict())
    consecutive_tails_data_percentage = {
        number: consecutive_tails_percentages[number] if number in consecutive_tails_percentages else 0
        for number in range(0, len(df.keys()) + 1)
    }

    # Count the number of max consecutive tails
    consecutive_tails_count = consecutive_tails.value_counts().to_dict()
    consecutive_tails_data = {
        number: consecutive_tails_count[number] if number in consecutive_tails_count else 0
        for number in range(0, len(df.keys()) + 1)
    }

    return dict(
        mean=dict(
            heads=consecutive_heads_mean,
            tails=consecutive_tails_mean,
        ),
        std=dict(
            heads=consecutive_heads_std,
            tails=consecutive_tails_std,
        ),
        percentages=dict(
            heads=consecutive_heads_data_percentage,
            tails=consecutive_tails_data_percentage,
        ),
        data=dict(
            heads=consecutive_heads_data,
            tails=consecutive_tails_data,
        )
    )
