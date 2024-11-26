import random
import string
import requests
from data import ENDPOINTS

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data(email_suffix="@example.com"):
    email = f"{generate_random_string(10)}{email_suffix}"
    password = generate_random_string(12)
    name = generate_random_string(8)
    return {"email": email, "password": password, "name": name}

def restore_user_data(email, original_data):
    response = requests.patch(ENDPOINTS["user"], json=original_data)
    if response.status_code == 200:
        print(f"User {email} data restored successfully.")
    else:
        print(f"Failed to restore user data for {email}. Response: {response.text}")


def delete_user(email, password):
    access_token = get_access_token(email, password)
    response = requests.delete(ENDPOINTS["user"], headers={"Authorization": f"Bearer {access_token}"})



def get_access_token(email, password):
    response = requests.post(ENDPOINTS["login"], json={
        "email": email,
        "password": password,
    })
    return response.json().get("accessToken")


