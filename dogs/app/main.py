from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder


###########################################
from pydantic import BaseModel, Field


class DogSchema(BaseModel):
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
database = client.dogs
dogs_collection = database.get_collection("dogs_collection")


def dog_helper(dog) -> dict:
    return {
        "id": str(dog["_id"]),
        "name": dog["name"],
        "color": dog["color"],
    }


async def retrieve_dogs():
    print("in retrieve dogs")
    dogs = []
    async for dog in dogs_collection.find():
        print("in retrieve dogs async")
        dogs.append(dog_helper(dog))
    return dogs


async def add_dog(dog_data: dict) -> dict:
    dog = await dogs_collection.insert_one(dog_data)
    new_dog = await dogs_collection.find_one({"_id": dog.inserted_id})
    return dog_helper(new_dog)


##################################
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to this fantastic app!"}


@app.get("/dogs")
async def get_all_dogs():
    dogs = await retrieve_dogs()
    if dogs:
        return response_model(dogs, "Dogs data retrieved successfully")
    return response_model(dogs, "Empty list returned")


@app.post("/dogs", response_description="Dog data added into the database")
async def add_dog_data(dog: DogSchema = Body(...)):
    dog = jsonable_encoder(dog)
    new_dog = await add_dog(dog)
    return response_model(new_dog, "Dog added successfully.")