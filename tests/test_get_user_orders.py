import requests
import allure
from data import ENDPOINTS, EXISTING_USER

class TestUserOrders:

    @staticmethod
    def login(user_data):
        response = requests.post(ENDPOINTS["login"], json=user_data)
        return response

    @allure.step("Авторизация пользователя")
    def test_get_orders_authorized(self):
        auth_response = self.login(EXISTING_USER)
        assert auth_response.status_code == 200, f"Ошибка при авторизации: {auth_response.text}"

        auth_token = auth_response.json().get("accessToken")
        assert auth_token, "Токен отсутствует"

        token = auth_token.split(' ')[1] if ' ' in auth_token else auth_token
        assert token, "Токен имеет неверный формат или отсутствует"

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(ENDPOINTS["orders"], headers=headers)
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

    @allure.step("Попытка получения заказов без авторизации")
    def test_get_orders_unauthorized(self):
        response = requests.get(ENDPOINTS["orders"])
        assert response.status_code == 401, f"Ожидался статус 401 (неавторизован), получен {response.status_code}"
        assert response.json().get(
            "message") == "You should be authorised", f"Неожиданное сообщение: {response.json().get('message')}"
