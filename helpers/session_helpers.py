from flask import session
from bson import ObjectId

def get_session_user_object_id():
    if 'user_data' in session:
        return ObjectId(session['user_data']['_id']["$oid"])
    return None

def get_session_user_id():
    if 'user_data' in session:
        return session['user_data']['_id']["$oid"]
    return None

def is_user_logged_in():
    return 'user_data' in session
    
def clear_session():
    return session.clear()