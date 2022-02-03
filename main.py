# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()


# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    # Try api in documentation
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Federico",
                "last_na,e": "Rosero",
                "age": 18,
                "hair_color": "black",
                "is_married": False
            }
        }


class Location(BaseModel):
    city: str
    state: str
    country: str


@app.get("/")
def home():
    return {"Hello": "World"}


# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validation: Query Parameters

@app.get("/person/detail")
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title="Person Name",
            description="This is person name. It´s between 1 and 50 characters",
        ),
        age: str = Query(
            ...,
            title="Person Age",
            description="This is the person age. It´s required"
        )
):
    return {name: age}


# Validation: Path parameters

@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(
            ...,
            gt=0,
            title="Person Id",
            description="This is the person id, It´s required"
        )
):
    return {person_id: "It exists!"}


# Validation: Body parameters

@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            ...,
            gt=0,
            title="Person Id",
            description="This is the person id",
        ),
        person: Person = Body(...),
        location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())

    return results
