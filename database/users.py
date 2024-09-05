from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from bson import ObjectId

uri = "mongodb+srv://admin:admin@cluster0.gkcrc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))

chatAppDb = client["chatApp"]
users = chatAppDb.users
my_id_string = "66d9fd1b2f408a1a0342afda"
def get_my_data(id):
    my_id_object = ObjectId(id)
    return users.find_one({"_id": my_id_object})
    
my_data = get_my_data(my_id_string)


def add_to_used_chatbots(id):
    id = ObjectId(id)
    used_chatbots = my_data["used_chatbots"]
    if id not in used_chatbots:
        used_chatbots.append(id)
        users.update_one(
            { "_id":my_data["_id"]  }
            , { "$set": { "used_chatbots": used_chatbots } }
            )

def get_my_used_chatbots():
    return list(chatAppDb.chat_bots.find({"_id": {"$in": my_data["used_chatbots"]}}))