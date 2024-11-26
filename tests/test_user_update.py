import requests
import allure
from data import ENDPOINTS, EXISTING_USER
from helpers.user_helpers import restore_user_data

class TestUserUpdate:

    @allure.feature('Обновление данных пользователя')
    @allure.story('Успешное обновление данных с авторизацией')
    def test_update_user_data_with_authorization(self):
        with allure.step('Отправляем запрос на авторизацию с существующими данными'):
            response = requests.post(ENDPOINTS["login"], json=EXISTING_USER)

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        access_token = response.json().get("accessToken")
        assert access_token, "Не удалось получить accessToken из ответа."

        token = access_token.split(' ')[1] if ' ' in access_token else access_token

        new_user_data = {
            "email": EXISTING_USER["email"],
            "name": "New Name"
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        with allure.step('Отправляем запрос на обновление данных пользователя'):
            response = requests.patch(ENDPOINTS["user"], json=new_user_data, headers=headers)

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get("success") is True, "Ожидалось 'success': True"
        assert response.json().get("user").get("email") == new_user_data["email"], \
            f"Ожидался новый email: {new_user_data['email']}, получен: {response.json().get('user').get('email')}"
        assert response.json().get("user").get("name") == new_user_data["name"], \
            f"Ожидалось новое имя: {new_user_data['name']}, получено: {response.json().get('user').get('name')}"

        with allure.step('Восстанавливаем данные пользователя'):
            restore_user_data(EXISTING_USER["email"], EXISTING_USER)

    @allure.feature('Обновление данных пользователя')
    @allure.story('Неуспешное обновление данных без авторизации')
    def test_update_user_data_without_authorization(self):
        new_user_data = {
            "email": EXISTING_USER["email"],
            "name": "New Name"
        }

        with allure.step('Отправляем запрос на обновление данных без авторизации'):
            response = requests.patch(ENDPOINTS["user"], json=new_user_data)

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get("success") is False, \
            f"Ожидалось 'success': False, получен: {response.json().get('success')}"
        assert response.json().get("message") == "You should be authorised", \
            f"Ожидалось сообщение 'You should be authorised', получено: {response.json().get('message')}"
