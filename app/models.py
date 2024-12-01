from pydantic import BaseModel, Field, ConfigDict, GetCoreSchemaHandler
from typing import Optional, Annotated
from bson import ObjectId
from typing import Any
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, (str, ObjectId)):
            raise ValueError("Invalid ObjectId")
        
        if isinstance(v, str):
            v = ObjectId(v)
        
        return v

    @classmethod
    def __get_pydantic_core_schema__(
        cls, 
        source_type: Any, 
        handler: GetCoreSchemaHandler
    ):
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(cls.validate)
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x),
                return_schema=core_schema.str_schema()
            )
        )

class Address(BaseModel):
    city: str
    country: str

class StudentCreate(BaseModel):
    name: str
    age: int
    address: Address

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

class StudentInResponse(BaseModel):
    id: Annotated[PyObjectId, Field(alias="_id")]
    name: str
    age: int
    address: Address

    model_config = ConfigDict(
        json_schema_extra={'example': {
            "id": "507f1f77bcf86cd799439011",
            "name": "John Doe",
            "age": 25,
            "address": {
                "city": "New York",
                "country": "USA"
            }
        }},
        populate_by_name=True,
        arbitrary_types_allowed=True
    )