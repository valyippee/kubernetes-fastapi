from typing import Union
from fastapi import FastAPI, Body
# from model import Cats, ResponseModel, CatSchema
# from database import retrieve_cats, add_cat
from fastapi.encoders import jsonable_encoder


###########################################
from pydantic import BaseModel, Field


class CatSchema(BaseModel):
    name: str = Field(...)
    color: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "color": "brown",
            }
        }


def response_model(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


################################
import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DETAILS = "mongodb://user:password@mongo-db:27017/"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.cats
cats_collection = database.get_collection("cats_collection")


def cat_helper(cat) -> dict:
    return {
        "id": str(cat["_id"]),
        "name": cat["name"],
        "color": cat["color"],
    }


async def retrieve_cats():
    print("in retrieve cats")
    cats = []
    async for cat in cats_collection.find():
        print("in retrieve cats async")
        cats.append(cat_helper(cat))
    return cats


async def add_cat(cat_data: dict) -> dict:
    cat = await cats_collection.insert_one(cat_data)
    new_cat = await cats_collection.find_one({"_id": cat.inserted_id})
    return cat_helper(new_cat)


##################################
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get("/cats")
async def get_all_cats():
    cats = await retrieve_cats()
    if cats:
        return response_model(cats, "Cats data retrieved successfully")
    return response_model(cats, "Empty list returned")


@app.post("/cats", response_description="Cat data added into the database")
async def add_cat_data(cat: CatSchema = Body(...)):
    cat = jsonable_encoder(cat)
    new_cat = await add_cat(cat)
    return response_model(new_cat, "Cat added successfully.")