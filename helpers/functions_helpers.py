from bson import json_util
import json
import hashlib

def parse_json(data):
    return json.loads(json_util.dumps(data))

def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()