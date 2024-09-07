from dotenv import load_dotenv,find_dotenv
import sys
import os
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
chats = chatAppDb.chats
deleted_chats = chatAppDb.deleted_chats

def insert_message(message,response,date):
    my_id_object = get_session_user_object_id()
    return chats.insert_one({"message":message,"date":date,"response":response,"owner":my_id_object,"model_nickname":response.get('model', 'unknown') })
    
def get_chat_history(model_nickname):
    my_id_object = get_session_user_object_id()
    return list(chats.find({"owner":my_id_object ,"model_nickname":model_nickname}))

def clear_chat_history(model_nickname):
    my_id_object = get_session_user_object_id()
    chats_to_delete = list(chats.find({"owner":my_id_object ,"model_nickname":model_nickname}))
    if len(chats_to_delete)>0:
        inserted_ids = deleted_chats.insert_many(chats_to_delete)
        if inserted_ids:
            chats.delete_many({"owner":my_id_object ,"model_nickname":model_nickname})
        return True
    else:
        return None

#deleted_chats.delete_many({})