from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.server_api import ServerApi

cfg = dotenv_values(".env")

client = MongoClient(cfg.get('URI'), server_api=ServerApi('1'))
db = client["ClientBugReport"]
collection = db["DocumentInfo"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise