# db.py
from pymongo import MongoClient
import os

# Use environment variable for MongoDB URI
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB using the URI
client = MongoClient(MONGO_URI)

db = client["student"]
students_collection = db.students