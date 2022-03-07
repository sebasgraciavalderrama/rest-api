from werkzeug.security import hmac
from user import User

users = [
    User(1, 'sebas', 'abc123')
]

username_mapping = {u.username: u for u in users} # Set comprehension
userid_mapping = {u.id: u for u in users} # Set comprehension

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
