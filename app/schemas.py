from pydantic import BaseModel
from typing import List
from .models import StudentResponse

class StudentListResponse(BaseModel):
    data: List[StudentResponse]