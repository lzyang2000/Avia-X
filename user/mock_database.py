import os
import pickle

file_path = os.path.dirname(os.path.abspath(__file__)) + '/user_database.p'
data = pickle.load(open(file_path, 'rb'))

def save(user):
    data[user.id] = { 'username': user.info.username, 'birthday': user.info.birthday, 'preference': user.info.preference, 'history': user.info.history, 'on_board' : user.info.on_board}
    pickle.dump(data, open(file_path, 'wb'))

def find(user_id=None):
    if (user_id):
        return data[user_id]
    return data

def clear():
    data = {}
    pickle.dump(data, open(file_path, 'wb'))
