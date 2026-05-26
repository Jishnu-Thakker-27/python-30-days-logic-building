import json

def load_task():
    with open("tasks.json") as f:
        data=json.load(f)
    return data

def save_task(tasks):
    with open("tasks.json","w") as f:
        json.dump(tasks,f)
