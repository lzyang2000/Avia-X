import os
import pickle

file_path = os.path.dirname(os.path.abspath(__file__)) + '/user_database.p'
data = pickle.load(open(file_path, 'rb'))

def save(user):
    data[user.username] = { 'birthday': user.info.birthday, 'preference': user.info.preference, 'history': user.info.history}
    pickle.dump(data, open(file_path, 'wb'))

def find(username=None):
    if (username):
        return data[username]
    return data

def clear():
    data = {}
    pickle.dump(data, open(file_path, 'wb'))
