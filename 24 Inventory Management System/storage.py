import json
def load():
    with open("products.json") as f:
        data=json.load(f)
    return data