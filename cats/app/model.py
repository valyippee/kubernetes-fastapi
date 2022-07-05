# from pydantic import BaseModel, Field
#
#
# class Cats(BaseModel):
#     name: str
#     color: str
#
#
# class CatSchema(BaseModel):
#     name: str = Field(...)
#     color: str = Field(...)
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "John",
#                 "color": "brown",
#             }
#         }
#
#
# def ResponseModel(data, message):
#     return {
#         "data": [data],
#         "code": 200,
#         "message": message,
#     }