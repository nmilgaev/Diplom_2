import allure
from helpers.api_requests import login_user, update_user_data, restore_user_data  # Используем функции из api_requests
from data import EXISTING_USER

@allure.feature('Обновление данных пользователя')
@allure.story('Тестирование обновления данных пользователя')
class TestUserUpdate:

    @allure.title('Тест успешного обновления данных с авторизацией')
    def test_update_user_data_with_authorization(self):
        with allure.step('Отправляем запрос на авторизацию с существующими данными'):
            response = login_user(EXISTING_USER)

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        access_token = response.json().get("accessToken")
        assert access_token, "Не удалось получить accessToken из ответа."

        token = access_token.split(' ')[1] if ' ' in access_token else access_token

        new_user_data = {
            "email": EXISTING_USER["email"],
            "name": "New Name"
        }

        with allure.step('Отправляем запрос на обновление данных пользователя'):
            response = update_user_data(new_user_data, token)

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get("success") is True, "Ожидалось 'success': True"
        assert response.json().get("user").get("email") == new_user_data["email"], \
            f"Ожидался новый email: {new_user_data['email']}, получен: {response.json().get('user').get('email')}"
        assert response.json().get("user").get("name") == new_user_data["name"], \
            f"Ожидался новое имя: {new_user_data['name']}, получено: {response.json().get('user').get('name')}"

        with allure.step('Восстанавливаем данные пользователя'):
            restore_user_data(EXISTING_USER["email"], EXISTING_USER)

    @allure.title('Тест неуспешного обновления данных без авторизации')
    def test_update_user_data_without_authorization(self):
        new_user_data = {
            "email": EXISTING_USER["email"],
            "name": "New Name"
        }

        with allure.step('Отправляем запрос на обновление данных без авторизации'):
            response = update_user_data(new_user_data)

        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"
        assert response.json().get("success") is False, \
            f"Ожидалось 'success': False, получен: {response.json().get('success')}"
        assert response.json().get("message") == "You should be authorised", \
            f"Ожидалось сообщение 'You should be authorised', получено: {response.json().get('message')}"
