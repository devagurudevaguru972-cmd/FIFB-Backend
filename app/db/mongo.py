import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
print(client.list_database_names())

db = client["chatbot"]

chat_collection = db["chat_history"]

user_collection = db["users"]