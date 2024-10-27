import requests
import json

def test_save_endpoint():
    url = "http://127.0.0.1:8000/api/save/"
    data = {
        "username": "test_user",
        "file_path": "/test/path/scene.blend"
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_save_endpoint()