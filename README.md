# Student Management API

Link https://fastapi-mongodb-vys8.onrender.com/

## Overview
A robust FastAPI-based backend service for managing student records using MongoDB, designed for scalable and efficient student data operations.

## Features
- Create, read, update, and delete student records
- Filter students by country and minimum age
- Comprehensive data validation
- MongoDB integration
- RESTful API design

## Prerequisites
- Python 3.8+
- FastAPI
- PyMongo
- Pydantic
- MongoDB Atlas account

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/student-management-api.git
cd student-management-api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB
- Create a MongoDB Atlas cluster
- Set `MONGO_URI` environment variable with your connection string

## API Endpoints

### Create Student
- **Endpoint:** `POST /students`
- **Request Body:** 
  ```json
  {
    "name": "string",
    "age": 0,
    "address": {
      "city": "string", 
      "country": "string"
    }
  }
  ```
- **Response:** `{"id": "student_id"}`

### List Students
- **Endpoint:** `GET /students`
- **Query Parameters:** 
  - `country`: Filter by country
  - `age`: Minimum age filter
- **Response:** 
  ```json
  {
    "data": [
      {
        "name": "string",
        "age": 0
      }
    ]
  }
  ```

### Get Student by ID
- **Endpoint:** `GET /students/{id}`
- **Response:** 
  ```json
  {
    "name": "string",
    "age": 0,
    "address": {
      "city": "string",
      "country": "string"
    }
  }
  ```

### Update Student
- **Endpoint:** `PATCH /students/{id}`
- **Request Body:** Partial student update
- **Response:** `{}`

### Delete Student
- **Endpoint:** `DELETE /students/{id}`
- **Response:** `{}`

## Running the Application
```bash
uvicorn app.main:app --reload
```

## Testing
```bash
pytest
```

## Deployment
- Deploy on platforms like Heroku, AWS, or Google Cloud
- Ensure environment variables are set
- Use production WSGI server like Gunicorn

## Error Handling
- 400: Invalid input
- 404: Resource not found
- 500: Server errors

## Security Considerations
- Use environment variables for credentials
- Implement authentication/authorization
- Validate and sanitize input data
