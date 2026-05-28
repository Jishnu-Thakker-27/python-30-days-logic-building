import json

def load():
    try:
        with open("products.json") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    except json.JSONDecodeError:
        data = []
    return data

def save(products):
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)