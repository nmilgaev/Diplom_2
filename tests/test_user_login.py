import allure
from helpers.api_requests import login_user
from data import EXISTING_USER, INVALID_USER

@allure.feature('Авторизация пользователя')
@allure.story('Тестирование различных сценариев авторизации')
class TestUserLogin:

    @allure.title('Тест успешного входа с корректными данными')
    def test_login_successful(self, login_user):
        with allure.step('Отправляем запрос на вход с существующими данными'):
            response = login_user(EXISTING_USER)

        with allure.step('Проверяем успешный ответ'):
            assert response.status_code == 200, \
                f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"
            response_json = response.json()
            assert response_json.get("success") is True, \
                f"Ожидался 'success': True, получен {response_json.get('success')}"
            assert "accessToken" in response_json, \
                f"В ответе отсутствует accessToken. Ответ: {response_json}"
            assert "refreshToken" in response_json, \
                f"В ответе отсутствует refreshToken. Ответ: {response_json}"
            assert "user" in response_json, \
                f"В ответе отсутствуют данные пользователя. Ответ: {response_json}"

    @allure.title('Тест неуспешного входа с неверными данными')
    def test_login_invalid_credentials(self, login_user):
        with allure.step('Отправляем запрос на вход с неверными данными'):
            response = login_user(INVALID_USER)

        with allure.step('Проверяем ошибку авторизации'):
            assert response.status_code == 401, \
                f"Ожидался код 401, получен {response.status_code}. Ответ: {response.text}"
            response_json = response.json()
            assert response_json.get("success") is False, \
                f"Ожидался 'success': False, получен {response_json.get('success')}"
            assert response_json.get("message") == "email or password are incorrect", \
                f"Ожидалось сообщение 'email or password are incorrect', получено: {response_json.get('message')}"
