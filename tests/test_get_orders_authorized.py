import requests
import allure
from urls import ORDER_URL

@allure.feature("Order API")
@allure.story("Get orders for authorized user")
@allure.title("Test getting orders for authorized user")
def test_get_orders_authorized(auth_token):
    """Тест получения заказов для авторизованного пользователя."""
    url = ORDER_URL
    headers = {"Authorization": f"Bearer {auth_token}"}

    with allure.step("Send request to get orders for authorized user"):
        response = requests.get(url, headers=headers)

    with allure.step("Validate response status and content"):
        # Проверяем, что статус ответа 200 (OK)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Проверяем, что в ответе есть список заказов
        response_json = response.json()
        assert "orders" in response_json, "Response does not contain 'orders'"

        # Прикрепляем тело ответа для отладки
        allure.attach(str(response_json), name="Response Body", attachment_type=allure.attachment_type.JSON)
