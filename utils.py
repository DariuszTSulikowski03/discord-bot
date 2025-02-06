import json

def load_config():
    """Loads bot configuration from a JSON file."""
    with open("config.json", "r") as file:
        return json.load(file)
