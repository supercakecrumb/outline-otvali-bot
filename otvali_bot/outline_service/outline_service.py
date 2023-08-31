import requests
import json

class outlineService:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user(self, client_id, server_id):
        url = f"{self.base_url}/create_user"
        payload = {
            'client_id': client_id,
            'server_id': server_id
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            print("User created successfully!")
            return json.loads(response.text)
        else:
            print(f"Failed to create user. Status Code: {response.status_code}")
            return None

    def delete_user(self, client_id, server_id):
        url = f"{self.base_url}/delete_user"
        payload = {
            'client_id': client_id,
            'server_id': server_id
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("User deleted successfully!")
            return json.loads(response.text)
        else:
            print(f"Failed to delete user. Status Code: {response.status_code}")
            return None

    def get_key(self, client_id, server_id) -> str:
        print(f"get_key with client={client_id} and server={server_id}")
        url = f"{self.base_url}/get_key"
        payload = {
            'client_id': client_id,
            'server_id': server_id
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("Key retrieved successfully!")
            response_json = json.loads(response.text)
            key_value = response_json.get('key', None)
            if key_value:
                print(f"Extracted key value: {key_value}")
                return key_value
            else:
                print("Key not found in the response.")
                return None
        else:
            print(f"Failed to retrieve key. Status Code: {response.status_code}")
            return None

