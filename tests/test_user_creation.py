import requests
import allure
from data import ENDPOINTS, EXISTING_USER, MISSING_FIELDS_USER

class TestUserCreation:

    @allure.step("Создание уникального пользователя")
    def test_create_unique_user(self, setup_unique_user):
        user_data = setup_unique_user

        response = requests.get(ENDPOINTS["user"], headers={"Authorization": f"Bearer {user_data['access_token']}"})

        assert response.status_code == 200, \
            f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        assert response.json().get("user", {}).get("email") == user_data["email"], \
            f"Ожидался email: {user_data['email']}, получен: {response.json().get('user', {}).get('email')}"


    @allure.step("Создание уже существующего пользователя")
    def test_create_existing_user(self):
        response = requests.post(ENDPOINTS["register_user"], json=EXISTING_USER)

        assert response.status_code == 403, \
            f"Ожидался код 403, получен {response.status_code}. Ответ: {response.text}"
        expected_response = {
            "success": False,
            "message": "User already exists"
        }
        assert response.json() == expected_response, \
            f"Ожидался ответ {expected_response}, получен: {response.json()}"

    @allure.step("Создание пользователя с отсутствующими обязательными полями")
    def test_create_user_missing_fields(self):
        incomplete_user = MISSING_FIELDS_USER.copy()
        incomplete_user["password"] = ""  # Убираем обязательное поле
        response = requests.post(ENDPOINTS["register_user"], json=incomplete_user)

        assert response.status_code == 403, \
            f"Ожидался код 403, получен {response.status_code}. Ответ: {response.text}"
        expected_response = {
            "success": False,
            "message": "Email, password and name are required fields"
        }
        assert response.json() == expected_response, \
            f"Ожидался ответ {expected_response}, получен: {response.json()}"
