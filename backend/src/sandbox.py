import pandas as pd
import numpy as np
from random import choice
from helper import CoinToss
from itertools import groupby

coin = [CoinToss.heads.value, CoinToss.tails.value]


def create_dataframe(num_throws: int) -> pd.DataFrame:
    num_rows = 100
    return pd.DataFrame(
        {"id" if k == 0 else k: [choice(coin) for _ in range(num_rows)]
         for k in range(1, num_throws + 1)}
    )


def len_iter(items):
    return sum(1 for _ in items)


def consecutive_values(data, bin_val):
    return list((len_iter(run) for val, run in groupby(data) if val == bin_val))


def after(df: pd.DataFrame) -> dict:
    print("dataframe\n", df.head())
    df["heads"] = df.apply(consecutive_values, bin_val="heads", axis=1)
    df["tails"] = df.apply(consecutive_values, bin_val="tails", axis=1)
    print("heads\n", df.head())
    return df


def analyse_throw(df: pd.DataFrame) -> dict:
    # This is the function, which is called when a GET request is made to /throws/<scenario>
    # Analyse the dataframe and return the analysis of the dataframe as a dictionary
    # Set the index of the dataframe to id

    # Count the number of heads and tails in the dataframe
    count_heads = df.apply(lambda x: (x == 'heads').sum())
    count_tails = df.apply(lambda x: (x == 'tails').sum())

    # Calculate the mean heads and mean tails
    mean_heads = (count_heads / (count_heads + count_tails)) * 100
    mean_tails = (count_tails / (count_heads + count_tails)) * 100

    # Look up if there are any repetitions in the dataframe
    dataframe = after(df)
    print("dataframe\n", df.head())
    print("heads\n", dataframe.head())
    # Other analysis of the dataframe
    pass  # <---- Your Code goes here --->

    # Return a dictionary with the mean heads and mean tails as keys and the values
    response = dict(
        mean_heads=mean_heads,
        mean_tails=mean_tails
    )

    return response


if __name__ == "__main__":
    # Create a dataframe with only heads
    test_df = create_dataframe(8)
    out = analyse_throw(test_df)
