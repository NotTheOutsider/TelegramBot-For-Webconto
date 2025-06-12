import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

load_dotenv()

try:
    client = AsyncMongoClient(os.getenv('URI'), server_api=ServerApi('1'))

    print("Successfully connected to MongoDB!")

    db = client["ClientBugReport"]
    collectionOrders = db["DocumentInfo"]
    collectionVerification = db["VerificationCodes"]
    collectionChats = db["ChatMasks"]
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise