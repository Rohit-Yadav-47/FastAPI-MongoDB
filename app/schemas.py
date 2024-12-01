# schemas.py
from pydantic import BaseModel
from typing import List
from .models import StudentInResponse

class StudentListResponse(BaseModel):
    data: List[StudentInResponse]