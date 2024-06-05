from typing import Type, Coroutine, Callable
import os
import numpy as np
from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .helper import *

'''
This file contains the code for the FastAPI server.
It also contains the code for the CRUD operations.
All Endpoints are automatically generated.

To add a throw scenario, you need to:
    - update the "throws" list (first line)
    
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
Change the throws list in the beginning of the file, if you want to change the number of throws.
'''

throws = [8, 10, 20, 30]  # Declare how many throws you want to create

# Get environment variables from.env file
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", 5432)
database = os.getenv("POSTGRES_DB", "coin_db")
user = os.getenv("POSTGRES_USER", "user")
password = os.getenv("POSTGRES_PASSWORD", "pass")


# engine = create_engine('postgresql+psycopg2://', creator=connect)
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# get Database Session gets overwritten on Testing
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create a base class for your models
Base = declarative_base()

# Creating models for 8, 10 and 20 throws
throws_models = {k: create_throw_class(k, base=Base) for k in throws}

# Bind the engine to the models
Base.metadata.create_all(bind=engine)

# Create a FastAPI instance
app = FastAPI()

origins = []

# Create the Schema for 8, 10 and 20 throws
throws_schema = {k: create_throw_class_crud(k) for k in throws}


# ==================================[ Editable Parts ]==================================
# To change the analysis of the dataframe, change the content of this function

def analyse_throw(df: pd.DataFrame) -> dict:
    # This is the function, which is called when a GET request is made to /throws/<scenario>
    # Analyse the dataframe and return the analysis of the dataframe as a dictionary
    df = df.set_index('id')  # Set the index of the dataframe to id

    # Create an empty dictionary and fill it with the analysis of the dataframe
    response = dict(total=df.shape[0])

    # count the mean of heads and tails
    response["count"] = count(df)

    # Look up if there are any consecutive in the dataframe
    response["consecutive"] = consecutive_values(df)

    # Other analysis of the dataframe
    pass  # <---- Your Code goes here --->

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
    # Read the data from the database and return it as a dataframe
    with engine.connect() as conn:
        df = pd.read_sql(
            sql=f"SELECT * FROM toss_{scenario}",
            con=conn.connection
        )
        # If dataframe is empty, return an empty dataframe
        if df.empty:
            print(f"database info: {db.info}")
            # When the database is empty, because the dataframe can't calculate
            raise ValueError('No throws found: Database is empty')
        elif df.shape[0] < 2:
            raise ValueError('Not Enough data: Database needs at least 2 throws')
        else:
            # Prevent division by zero
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.dropna()

        return df


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
        # Test
        path=f"/throws/{num_throws}",
        endpoint=generate_post_endpoint(num_throws, model),
        response_model=model,
        methods=["POST"]
    )

    # create a GET endpoint for each scenario
    app.add_api_route(
        path=f"/throws/{num_throws}",
        endpoint=generate_get_endpoint(num_throws),
        response_model=AnalysisResponse,
        methods=["GET"]
    )
