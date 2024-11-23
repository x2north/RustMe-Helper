import json 

def client_token():
    with open('config.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data["client_token"]
    
def client_version():
    with open('config.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data["version"]
    
    