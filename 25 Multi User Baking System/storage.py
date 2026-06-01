import json
def user_load():
    with open("users.json") as f:
        data=json.load(f)
    return data