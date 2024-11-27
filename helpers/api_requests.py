import requests
import allure
from data import ENDPOINTS

@allure.step("Регистрация пользователя")
def register_user(user_data):
    response = requests.post(ENDPOINTS["register_user"], json=user_data)
    return response

@allure.step("Получение access токена для пользователя")
def get_access_token(email, password):
    response = requests.post(ENDPOINTS["login"], json={
        "email": email,
        "password": password,
    })
    return response.json().get("accessToken")

@allure.step("Логин пользователя")
def login_user(user_data):
    response = requests.post(ENDPOINTS["login"], json=user_data)
    return response

@allure.step("Восстановление данных пользователя")
def restore_user_data(email, original_data):
    response = requests.patch(ENDPOINTS["user"], json=original_data)
    if response.status_code == 200:
        print(f"User {email} data restored successfully.")
    else:
        print(f"Failed to restore user data for {email}. Response: {response.text}")

@allure.step("Удаление пользователя")
def delete_user(email, password):
    access_token = get_access_token(email, password)
    response = requests.delete(ENDPOINTS["user"], headers={"Authorization": f"Bearer {access_token}"})
    if response.status_code == 200:
        print(f"User {email} deleted successfully.")
    else:
        print(f"Failed to delete user {email}. Response: {response.text}")

@allure.step("Получение заказов пользователя")
def get_user_orders(token=None):
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ENDPOINTS["orders"], headers=headers)
    return response

@allure.step("Создание заказа")
def create_order(order_data, token=None):
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}

    response = requests.post(ENDPOINTS["orders"], json=order_data, headers=headers)
    return response


@allure.step("Получение данных пользователя")
def get_user_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ENDPOINTS["user"], headers=headers)
    return response

@allure.step("Обновление данных пользователя")
def update_user_data(user_data, token=None):
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(ENDPOINTS["user"], json=user_data, headers=headers)
    return response