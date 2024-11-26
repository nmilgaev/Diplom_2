import requests
import allure
from data import EXISTING_USER, INGREDIENTS, ENDPOINTS


class TestOrder:
    @staticmethod
    def login(user_data):
        login_url = ENDPOINTS["login"]
        response = requests.post(login_url, json=user_data)
        return response

    @allure.step("Авторизация пользователя")
    def test_create_order_with_auth(self):
        auth_response = self.login(EXISTING_USER)
        assert auth_response.status_code == 200, f"Ошибка во время входа в систему: {auth_response.text}"

        auth_token = auth_response.json().get("accessToken")
        token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
        assert token, "Токен отсутствует или имеет неверный формат"


        order_data = {"ingredients": INGREDIENTS[:2]}  # Два ингредиента
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.post(ENDPOINTS["orders"], json=order_data, headers=headers)

        assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"
        assert response.json().get("success") is True, "Не удалось создать заказ"

    @allure.step("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        order_data = {"ingredients": INGREDIENTS[:2]}  # Два ингредиента
        response = requests.post(ENDPOINTS["orders"], json=order_data)

        assert response.status_code == 200, f"Ожидаемй ответ 401 Unauthorized, но вернулся {response.status_code}"

    @allure.step("Создание заказа с ингредиентами")
    def test_create_order_with_ingredients(self):
        order_data = {"ingredients": INGREDIENTS[:2]}  # Два ингредиента
        response = requests.post(ENDPOINTS["orders"], json=order_data)

        assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"
        assert response.json().get("success") is True, "Не удалось создать заказ"

    @allure.step("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        order_data = {}  # Без ингредиентов
        response = requests.post(ENDPOINTS["orders"], json=order_data)

        assert response.status_code == 400, f"Ожидаемый ответ 400 Bad Request, но вернулся {response.status_code}"
        assert response.json().get("success") is False, "Ожидаемая ошибка из-за отсутствия ингредиентов"

    @allure.step("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self):
        order_data = {"ingredients": ["44445"]}  # Неверный хеш ингредиента
        response = requests.post(ENDPOINTS["orders"], json=order_data)

        assert response.status_code == 500, f"Ожидаемый ответ 500 Internal Server Error, но вернулся {response.status_code}"
