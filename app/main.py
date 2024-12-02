from fastapi import FastAPI, HTTPException, Path, Query, Body
from fastapi.responses import JSONResponse
from typing import Optional, List

from app.models import (
    StudentCreate, 
    StudentUpdate, 
    StudentCreateResponse, 
    StudentListResponse, 
    StudentDetailResponse
)
from app.crud import (
    create_student, 
    get_students, 
    get_student_by_id, 
    update_student, 
    delete_student
)

app = FastAPI(
    title="Backend Intern Hiring Task",
    version="1.0.0",
    description="Student Management API"
)

@app.post("/students", status_code=201, response_model=StudentCreateResponse)
def create_student_endpoint(student: StudentCreate):
    try:
        student_id = create_student(student)
        return {"id": student_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students", response_model=StudentListResponse)
def list_students(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Minimum age filter")
):
    try:
        students = get_students(country, age)
        return {"data": students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/students/{id}", response_model=StudentDetailResponse)
def fetch_student(id: str = Path(..., description="Student ID")):
    try:
        student = get_student_by_id(id)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/students/{id}", status_code=204)
def update_student_endpoint(
    id: str = Path(..., description="Student ID"),
    student_update: StudentUpdate = Body(...)
):
    try:
        success = update_student(id, student_update)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        return JSONResponse(status_code=204, content={})
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid student ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.delete("/students/{id}", status_code=200)
def delete_student_endpoint(id: str = Path(..., description="Student ID")):
    try:
        success = delete_student(id)
        if not success:
            raise HTTPException(status_code=404, detail="Student not found")
        return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
