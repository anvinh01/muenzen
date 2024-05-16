from typing import Type, Coroutine, Any, Callable

from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from .helper import *

'''
This file contains the code for the FastAPI server.
It also contains the code for the CRUD operations.
All Endpoints are automatically generated.

To add a throw scenario, you need to:
    - update the throws list
    
To add more analyses, you need to:
    - update the analyse_throw function
    - add the data into the response dictionary
    
The POST-Endpoint are automatically generated.
It allows a POST-Request to "/throws/<num_throws>" with a JSON-Body containing
 {"throw_<num_throws>": "heads | tails", ...}

Example:
{
    "throw_1": "heads",
    "throw_2": "tails",
    "throw_3": "heads",
    "throw_4": "tails",
    ...
}

The helper functions are found in the helper.py file.
'''

# Setup Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./throws.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# get Database Session gets overwritten on Testing
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


throws = [8, 10, 20]  # Declare how many throws you want to create

# Create a base class for your models
Base = declarative_base()

# Creating models for 8, 10 and 20 throws
throws_models = {k: create_throw_class(k, base=Base) for k in throws}

# Bind the engine to the models
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

# Create the Schema for 8, 10 and 20 throws
throws_schema = {k: create_throw_class_crud(k) for k in throws}


# ==================================[ Editable Parts ]==================================
# To change the analysis of the dataframe, change the content of this function

def analyse_throw(df: pd.DataFrame) -> dict:
    # This is the function, which is called when a GET request is made to /throws/<scenario>
    # Analyse the dataframe and return the analysis of the dataframe as a dictionary
    df = df.set_index('id')  # Set the index of the dataframe to id

    # Count the number of heads and tails in the dataframe
    count_heads = df.apply(lambda x: (x == 'heads').sum())
    count_tails = df.apply(lambda x: (x == 'tails').sum())

    # Calculate the mean heads and mean tails
    mean_heads = (count_heads / (count_heads + count_tails)) * 100
    mean_tails = (count_tails / (count_heads + count_tails)) * 100

    # Other analysis of the dataframe
    pass  # <---- Your Code goes here --->

    # Return a dictionary with the mean heads and mean tails as keys and the values
    response = dict(
        mean_heads=mean_heads,
        mean_tails=mean_tails
    )

    return response


# =================================[ Creating API-Endpoints ]==================================
# Create a function, which gets called, when a POST request is made to /throws/<scenario>
def create_throw(db: Session, scenario: int, throw_data: BaseModel):
    # Check if the scenario is valid
    if scenario not in throws_models.keys():
        raise ValueError('Num of throws can only be 8 or 10')

    # If it's valid, create a new throw object and add it to the database
    db_throw = throws_models[scenario](**throw_data.model_dump())
    db.add(db_throw)
    db.commit()
    db.refresh(db_throw)

    # Return the newly created throw object
    return db_throw


def get_throw(db: Session, scenario: int):
    # This function gets called, when a GET request is made to /throws/<scenario>
    # Return the dataframe of the throws with the given scenario
    if scenario not in throws_models.keys():
        raise ValueError('Num of throws can only be 8 or 10')
    return pd.read_sql(f"SELECT * FROM toss_{scenario}", db.bind)


# =================================[ Creating API-Endpoints ]==================================
# These Functions are used to create the API-Endpoints
# The async endpoint function will be used and is the code which will run, when the endpoint is called

def generate_post_endpoint(scenario: int, model_type: Type[BaseModel]):
    # Create a Throw in the Database, upon a post request is made to /throws/<scenario>
    async def endpoint(throw: model_type, db: Session = Depends(get_db)):
        return create_throw(db, scenario, throw_data=throw)

    return endpoint


def generate_get_endpoint(scenario: int) -> Callable[[Session], Coroutine[Any, Any, Any]]:
    # return an analysis of the throws, upon a get request is made to /throws/<scenario>
    async def endpoint(db: Session = Depends(get_db)):
        data = get_throw(db, scenario)  # read the data from the database into a dataframe
        result = analyse_throw(data)  # analyse the dataframe
        return result

    return endpoint


# Create the API-Endpoints for 8, 10 and 20 throws
# Each will have a POST and a GET endpoint
for num_throws, model in throws_schema.items():
    # create a POST endpoint for each scenario
    app.add_api_route(
        path=f"/throws/{num_throws}",
        endpoint=generate_post_endpoint(num_throws, model),
        response_model=model,
        methods=["POST"]
    )

    # create a GET endpoint for each scenario
    app.add_api_route(
        path=f"/throws/{num_throws}",
        endpoint=generate_get_endpoint(num_throws),
        methods=["GET"]
    )
