import json

def load_sent_tweets(file_path):
    try:
        with open(file_path, 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_sent_tweets(sent_tweets, file_path):
    with open(file_path, 'w') as f:
        json.dump(list(sent_tweets), f)