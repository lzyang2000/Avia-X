import json
import os

file_path = os.path.dirname(os.path.abspath(__file__)) + '/theme_database.json'
with open(file_path, 'r') as fp:
    data = json.load(fp)

def save(user, theme, customized_theme):
    user_customize_str = user.username + theme
    data[user_customize_str] = { 'theme' : customized_theme }
    with open(file_path, 'w') as fp:
        json.dump(data, fp)

def find(customized_theme=None):
    if (customized_theme):
        return data[customized_theme]
    return data

def clear():
    data = {}
    with open(file_path, 'w') as fp:
        json.dump(data, fp)
