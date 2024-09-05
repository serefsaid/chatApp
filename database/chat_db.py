from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import ObjectId

uri = "mongodb+srv://admin:admin@cluster0.gkcrc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

chatAppDb = client["chatApp"]
chats = chatAppDb.chats


def insert_message(message,response):
    return chats.insert_one({"message":message,"response":response })

#python chat.py