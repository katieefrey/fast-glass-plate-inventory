# from pydantic import BaseModel, Field
# from bson import ObjectId



# class ItemBase(BaseModel):
#     title: str
#     description: str = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


# class PlateBase(BaseModel):
#     identifier: str
#     archive: str


# # class PlateCreate(PlateBase):
# #     pass


# class Plate(ItemBase):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     identifier: str
#     archive: str

#     class Config:
#         orm_mode = True
