import allure
from helpers.api_requests import login_user, get_user_data, register_user
from data import EXISTING_USER, MISSING_FIELDS_USER

@allure.feature("Создание пользователя")
@allure.story("Тестирование создания пользователей с различными условиями")
class TestUserCreation:

    @allure.title("Тест создания уникального пользователя")
    def test_create_unique_user(self, setup_unique_user):
        user_data = setup_unique_user

        auth_response = login_user(user_data)
        assert auth_response.status_code == 200, \
            f"Ошибка при авторизации: {auth_response.status_code}. Ответ: {auth_response.text}"

        auth_token = auth_response.json().get("accessToken")
        token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
        assert token, "Токен отсутствует или имеет неверный формат"

        response = get_user_data(token)

        assert response.status_code == 200, \
            f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        assert response.json().get("user", {}).get("email") == user_data["email"], \
            f"Ожидался email: {user_data['email']}, получен: {response.json().get('user', {}).get('email')}"

    @allure.title("Тест создания уже существующего пользователя")
    def test_create_existing_user(self):
        response = register_user(EXISTING_USER)

        assert response.status_code == 403, \
            f"Ожидался код 403, получен {response.status_code}. Ответ: {response.text}"
        expected_response = {
            "success": False,
            "message": "User already exists"
        }
        assert response.json() == expected_response, \
            f"Ожидался ответ {expected_response}, получен: {response.json()}"

    @allure.title("Тест создания пользователя с отсутствующими обязательными полями")
    def test_create_user_missing_fields(self):
        incomplete_user = MISSING_FIELDS_USER.copy()
        incomplete_user["password"] = ""  # Убираем обязательное поле
        response = register_user(incomplete_user)

        assert response.status_code == 403, \
            f"Ожидался код 403, получен {response.status_code}. Ответ: {response.text}"
        expected_response = {
            "success": False,
            "message": "Email, password and name are required fields"
        }
        assert response.json() == expected_response, \
            f"Ожидался ответ {expected_response}, получен: {response.json()}"
