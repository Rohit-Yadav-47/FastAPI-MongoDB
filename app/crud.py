from app.db import students_collection
from app.models import StudentCreate, StudentUpdate, StudentInResponse
from bson import ObjectId
from typing import Optional, List
from pymongo.errors import PyMongoError

def create_student(student: StudentCreate) -> StudentInResponse:
    try:
        student_dict = student.model_dump(exclude_unset=True)
        
        if 'address' in student_dict:
            student_dict['address'] = dict(student_dict['address'])
        
        result = students_collection.insert_one(student_dict)
        
        return StudentInResponse(
            id=result.inserted_id, 
            name=student_dict['name'], 
            age=student_dict['age'], 
            address=student_dict['address']
        )
    except PyMongoError as e:
        print(f"MongoDB Error during student creation: {e}")
        raise

def get_students(country: Optional[str] = None, age: Optional[int] = None) -> List[StudentInResponse]:
    try:
        query = {}
        if country:
            query['address.country'] = country
        if age is not None:
            query['age'] = {'$gte': age}
        
        students = list(students_collection.find(query))
        return [
            StudentInResponse(
                id=student['_id'], 
                name=student['name'], 
                age=student['age'], 
                address=student['address']
            ) for student in students
        ]  # Added closing bracket here
    except PyMongoError as e:
        print(f"MongoDB Error during student retrieval: {e}")
        raise

def get_student_by_id(student_id: str) -> Optional[StudentInResponse]:
    try:
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            return StudentInResponse(
                id=student['_id'], 
                name=student['name'], 
                age=student['age'], 
                address=student['address']
            )
        return None
    except PyMongoError as e:
        print(f"MongoDB Error during student retrieval: {e}")
        raise

def update_student(student_id: str, student_update: StudentUpdate) -> bool:
    try:
        update_data = student_update.model_dump(exclude_unset=True)
        
        if 'address' in update_data:
            update_data['address'] = dict(update_data['address'])
        
        result = students_collection.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except PyMongoError as e:
        print(f"MongoDB Error during student update: {e}")
        raise

def delete_student(student_id: str) -> bool:
    try:
        result = students_collection.delete_one({"_id": ObjectId(student_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        print(f"MongoDB Error during student deletion: {e}")
        raise