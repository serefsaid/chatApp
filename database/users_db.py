from dotenv import load_dotenv,find_dotenv
import os
import sys
import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import ObjectId
from flask import session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'helpers')))
from session_helpers import get_session_user_id, is_user_logged_in,get_session_user_object_id

load_dotenv(find_dotenv())

mongo_password = os.environ.get("MONGODB_PWD")
uri = f"mongodb+srv://admin:{mongo_password}@cluster0.gkcrc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

chatAppDb = client["chatApp"]
users = chatAppDb.users
def get_my_data():
    return users.find_one({"_id": get_session_user_object_id()})
    
def check_user(username,password):
    return users.find_one({"username": username,"password": password},{"username": 1})


def add_to_used_chatbots(id):
    id = ObjectId(id)
    my_data = get_my_data()
    used_chatbots = my_data["used_chatbots"]
    if id not in used_chatbots:
        used_chatbots.append(id)
        users.update_one(
            { "_id":my_data["_id"]  }
            , { "$set": { "used_chatbots": used_chatbots } }
            )

def get_used_chatbots():
    my_data = get_my_data()
    return list(chatAppDb.chat_bots.find({"_id": {"$in": my_data["used_chatbots"]}}))