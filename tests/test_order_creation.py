import allure
from data import INGREDIENTS, EXISTING_USER
from helpers.api_requests import create_order

@allure.feature("Создание заказа")
@allure.story("Тестирование функционала создания заказа с различными условиями")
class TestOrder:

    @allure.title("Тест создания заказа с авторизацией")
    def test_create_order_with_auth(self, login_user):
        auth_response = login_user(EXISTING_USER)
        assert auth_response.status_code == 200, f"Ошибка во время входа в систему: {auth_response.text}"

        auth_token = auth_response.json().get("accessToken")
        token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
        assert token, "Токен отсутствует или имеет неверный формат"

        order_data = {"ingredients": INGREDIENTS[:2]}  # Два ингредиента
        response = create_order(order_data, token)

        assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"
        assert response.json().get("success") is True, "Не удалось создать заказ"

    @allure.title("Тест создания заказа без авторизации")
    def test_create_order_without_auth(self):
        order_data = {"ingredients": INGREDIENTS[:2]}
        response = create_order(order_data)

        assert response.status_code == 200, f"Ожидаемый ответ 200, но вернулся {response.status_code}"

    @allure.title("Тест создания заказа с ингредиентами")
    def test_create_order_with_ingredients(self):
        order_data = {"ingredients": INGREDIENTS[:2]}
        response = create_order(order_data)

        assert response.status_code == 200, f"Ошибка при создании заказа: {response.text}"
        assert response.json().get("success") is True, "Не удалось создать заказ"

    @allure.title("Тест создания заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        order_data = {}

        response = create_order(order_data)

        assert response.status_code == 400, f"Ожидаемый ответ 400 Bad Request, но вернулся {response.status_code}"
        assert response.json().get("success") is False, "Ожидалась ошибка из-за отсутствия ингредиентов"

    @allure.title("Тест создания заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self):
        order_data = {"ingredients": ["44445"]}
        response = create_order(order_data)

        assert response.status_code == 500, f"Ожидаемый ответ 500 Internal Server Error, но вернулся {response.status_code}"
