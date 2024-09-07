from dotenv import load_dotenv,find_dotenv
import os
import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import ObjectId
from flask import session

load_dotenv(find_dotenv())

mongo_password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://admin:{mongo_password}@cluster0.gkcrc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

chatAppDb = client["chatApp"]
chat_bots = chatAppDb.chat_bots

def get_bot_data(nickname):
    data = chat_bots.find_one({"nickname": nickname})
    data["_id"] = str(data["_id"])#for being able to use with input
    return data

def insert_new_bot(nickname,name,image_url):
    {
        "nickname":nickname
        ,"name":name
        ,"image_url":image_url
    }
    chat_bot_id = chat_bots.insert_one(new_chat_bot)
    