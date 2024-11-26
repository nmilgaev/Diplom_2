import pytest
import requests
from helpers.user_helpers import generate_user_data, get_access_token, delete_user
from data import ENDPOINTS

@pytest.fixture
def setup_unique_user():
    user_data = generate_user_data()

    response = requests.post(ENDPOINTS["register_user"], json=user_data)

    access_token = get_access_token(user_data["email"], user_data["password"])

    token = access_token.split(' ')[1] if ' ' in access_token else access_token
    user_data["access_token"] = token

    yield user_data

    delete_user(user_data["email"], user_data["password"])


