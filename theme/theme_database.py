import json
import os

file_path = os.path.dirname(os.path.abspath(__file__)) + '/theme_database.json'
with open(file_path, 'r') as fp:
    data = json.load(fp)

SEPARATOR = '*^*'

def get_customized_name(username, theme_name):
    return username + SEPARATOR + theme_name

def belongs_to_user(customized_name, username):
    return customized_name.split(SEPARATOR)[0] == username

def extends_theme(customized_name, theme_name):
    return customized_name.split(SEPARATOR)[1] == theme_name

def save(user, customized_theme):
    user_customize_str = get_customized_name(user.username, customized_theme.name)
    data[user_customize_str] = customized_theme.to_dict()
    with open(file_path, 'w') as fp:
        json.dump(data, fp)

def find(user=None, theme_name=None):
    if user and theme_name:
        customized_name = get_customized_name(user.username, theme_name)
        if customized_name in data:
            return data[customized_name]
        return None
    if user:
        return { name: value for name, value in data.items() if belongs_to_user(name, user.username) }
    if theme_name:
        return { name: value for name, value in data.items() if extends_theme(name, theme_name) }
    return data

def clear():
    data = {}
    with open(file_path, 'w') as fp:
        json.dump(data, fp)
