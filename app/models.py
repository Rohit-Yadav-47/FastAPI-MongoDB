from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic_core import core_schema

class PyObjectId(ObjectId):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, (str, ObjectId)):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v) if isinstance(v, str) else v

    @classmethod
    def __get_pydantic_core_schema__(
        cls, 
        source_type: any, 
        handler: any
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
    city: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., gt=0, le=150)
    address: Address

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, gt=0, le=150)
    address: Optional[Address] = None

class StudentCreateResponse(BaseModel):
    id: str

class StudentResponse(BaseModel):
    name: str
    age: int

class StudentDetailResponse(StudentResponse):
    address: Optional[Address] = None

class StudentListResponse(BaseModel):
    data: List[StudentResponse]