# db.py
from pymongo import MongoClient
import os

# Use environment variable for MongoDB URI
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://computerfun200:O2txh6NJEPRx7bJN@cluster0.01s7n5q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Connect to MongoDB using the URI
client = MongoClient(MONGO_URI)

db = client["student"]
students_collection = db.students