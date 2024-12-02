from app.db import students_collection
from app.models import StudentCreate, StudentUpdate
from bson import ObjectId
from typing import Optional, List
from pymongo.errors import PyMongoError

def create_student(student: StudentCreate) -> str:
    try:
        student_dict = student.model_dump()
        result = students_collection.insert_one(student_dict)
        return str(result.inserted_id)
    except PyMongoError as e:
        raise RuntimeError(f"Error creating student: {str(e)}")

def get_students(country: Optional[str] = None, age: Optional[int] = None) -> List[dict]:
    try:
        query = {}
        if country:
            query['address.country'] = country
        if age is not None:
            query['age'] = {'$gte': age}
        
        students = list(students_collection.find(query))
        return [
            {
                "name": student['name'], 
                "age": student['age']
            } for student in students
        ]
    except PyMongoError as e:
        raise RuntimeError(f"Error retrieving students: {str(e)}")

def get_student_by_id(student_id: str) -> Optional[dict]:
    try:
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            return {
                "name": student['name'], 
                "age": student['age'],
                "address": student.get('address')
            }
        return None
    except PyMongoError as e:
        raise RuntimeError(f"Error retrieving student: {str(e)}")

def update_student(student_id: str, student_update: StudentUpdate) -> bool:
    try:
        object_id = ObjectId(student_id)
        update_data = {k: v for k, v in student_update.model_dump(exclude_unset=True).items() if v is not None}
        if not update_data:
            return False
        
        result = students_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        raise RuntimeError(f"Error updating student: {str(e)}")
    
def delete_student(student_id: str) -> bool:
    try:
        result = students_collection.delete_one({"_id": ObjectId(student_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        raise RuntimeError(f"Error deleting student: {str(e)}")