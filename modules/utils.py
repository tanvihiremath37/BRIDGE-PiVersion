import os
import json

# Get project base directory dynamically
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def abs_path(*paths):
    """
    Returns absolute path inside BRIDGE/ directory.
    Example: abs_path("models", "model.p")
    """
    return os.path.join(BASE_DIR, *paths)


def load_json(path):
    """
    Safely load JSON file and return content as dict.
    Returns {} if file missing or corrupted.
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}


def save_json(path, data):
    """
    Safely save a dictionary to JSON file.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def ensure_dir(path):
    """
    Create folder if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)
