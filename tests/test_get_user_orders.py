import allure
from data import EXISTING_USER
from helpers.api_requests import get_user_orders

@allure.feature("Заказы пользователя")
@allure.story("Получение заказов пользователя через авторизацию")
class TestUserOrders:

    @allure.title("Тест авторизации пользователя")
    def test_get_orders_authorized(self, login_user):
        auth_response = login_user(EXISTING_USER)
        assert auth_response.status_code == 200, f"Ошибка при авторизации: {auth_response.text}"

        auth_token = auth_response.json().get("accessToken")
        assert auth_token, "Токен отсутствует"

        token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
        assert token, "Токен имеет неверный формат или отсутствует"

        response = get_user_orders(token)
        assert response.status_code == 200, f"Ошибка при получении заказов: {response.text}"

        orders = response.json().get("orders")
        assert isinstance(orders, list), "Данные о заказах не являются списком"
        assert len(orders) <= 50, "Возвращено больше 50 заказов"
        assert "total" in response.json(), "Общее количество заказов не возвращено"
        assert "totalToday" in response.json(), "Общее количество заказов за сегодня не возвращено"
        assert response.json()["success"] is True, "Флаг успеха равен False"

        for order in orders:
            assert all(key in order for key in
                       ["ingredients", "status", "number", "createdAt", "updatedAt"]), "Отсутствуют поля заказа"

    @allure.title("Тест получения заказов без авторизации")
    def test_get_orders_unauthorized(self):
        response = get_user_orders()
        assert response.status_code == 401, f"Ожидался статус 401 (неавторизован), получен {response.status_code}"
        assert response.json().get("message") == "You should be authorised", f"Неожиданное сообщение: {response.json().get('message')}"
