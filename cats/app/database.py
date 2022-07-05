# import motor.motor_asyncio
# from bson.objectid import ObjectId
#
#
# MONGO_DETAILS = "mongodb://localhost:27017"
# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
# database = client.cats
# cats_collection = database.get_collection("cats_collection")
#
#
# def cat_helper(cat) -> dict:
#     return {
#         "id": str(cat["_id"]),
#         "name": cat["name"],
#         "color": cat["color"],
#     }
#
#
# async def retrieve_cats():
#     cats = []
#     async for cat in cats_collection.find():
#         cats.append(cats_collection(cat))
#     return cats
#
#
# async def add_cat(cat_data: dict) -> dict:
#     cat = await cats_collection.insert_one(cat_data)
#     new_cat = await cats_collection.find_one({"_id": cat.inserted_id})
#     return cat_helper(new_cat)
