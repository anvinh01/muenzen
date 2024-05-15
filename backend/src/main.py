from typing import Type, Coroutine, Any, Callable

from fastapi import FastAPI, Depends
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from .helper import *

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


# Create a function, which gets called, when a POST request is made to /throws/<scenario>
def create_throw(db: Session, scenario: int, throw_data: any):
    # Check if the scenario is valid
    if scenario not in throws_models.keys():
        raise ValueError('Num of throws can only be 8 or 10')

    # If it's valid, create a new throw object and add it to the database
    db_throw = throws_models[scenario](**throw_data.model_dump())
    db.add(db_throw)
    db.commit()
    db.refresh(db_throw)
    return db_throw


def get_throw(db: Session, scenario: int):
    if scenario not in throws_models.keys():
        raise ValueError('Num of throws can only be 8 or 10')
    return pd.read_sql(f"SELECT * FROM toss_{scenario}", db.bind)


def generate_post_endpoint(scenario: int, model_type: Type[BaseModel]):
    async def endpoint(throw: model_type, db: Session = Depends(get_db)):
        return create_throw(db, scenario, throw_data=throw)

    return endpoint


def generate_get_endpoint(scenario: int) -> Callable[[Session], Coroutine[Any, Any, Any]]:
    async def endpoint(db: Session = Depends(get_db)):
        data = get_throw(db, scenario)
        df = pd.DataFrame(data)
        print(df)
        df = df.set_index('id')
        count_heads = df.apply(lambda x: (x == 'heads').sum())
        count_tails = df.apply(lambda x: (x == 'tails').sum())
        mean_heads = (count_heads / (count_heads + count_tails)) * 100
        mean_tails = (count_tails / (count_heads + count_tails)) * 100
        return dict(mean_heads=mean_heads,
                    mean_tails=mean_tails)

    return endpoint


for num_throws, model in throws_schema.items():
    app.add_api_route(
        path=f"/throws/{num_throws}",
        endpoint=generate_post_endpoint(num_throws, model),
        response_model=model,
        methods=["POST"]
    )

    app.add_api_route(
        path=f"/throws/{num_throws}",
        endpoint=generate_get_endpoint(num_throws),
        methods=["GET"]
    )
