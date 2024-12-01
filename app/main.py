from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.models import StudentCreate, StudentUpdate
from app.schemas import StudentListResponse
from app.crud import (
    create_student, 
    get_students, 
    get_student_by_id, 
    update_student, 
    delete_student
)
from typing import Optional
from pymongo.errors import PyMongoError

app = FastAPI()

@app.exception_handler(PyMongoError)
async def mongodb_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal database error"}
    )

@app.post("/students", status_code=201)
async def create_student_api(student: StudentCreate):
    try:
        created_student = create_student(student)
        return created_student
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students", response_model=StudentListResponse)
async def list_students(country: Optional[str] = None, age: Optional[int] = None):
    try:
        students = get_students(country, age)
        return StudentListResponse(data=students)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/{student_id}")
async def fetch_student(student_id: str):
    try:
        student = get_student_by_id(student_id)
        if student:
            return student
        raise HTTPException(status_code=404, detail="Student not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/students/{student_id}")
async def update_student_api(student_id: str, student_update: StudentUpdate):
    try:
        success = update_student(student_id, student_update)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/students/{student_id}")
async def delete_student_api(student_id: str):
    try:
        success = delete_student(student_id)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))