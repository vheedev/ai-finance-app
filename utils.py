import json
import os

def load_user_categories(username):
    path = f"data/categories/{username}.json"
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)

def save_user_categories(username, categories):
    path = f"data/categories/{username}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(categories, f, indent=2)