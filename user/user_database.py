import json
import os

file_path = os.path.dirname(os.path.abspath(__file__)) + '/user_database.json'
with open(file_path, 'r') as fp:
    data = json.load(fp)

def save(user):
    data[user.username] = { 'birthday': user.info.birthday, 'preference': user.info.preference, 'history': user.info.history }
    with open(file_path, 'w') as fp:
        json.dump(data, fp)

def find(username=None):
    if (username):
        return data[username]
    return data

def clear():
    data = {}
    with open(file_path, 'w') as fp:
        json.dump(data, fp)
