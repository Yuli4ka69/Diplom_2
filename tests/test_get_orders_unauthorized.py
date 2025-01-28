import requests
import allure
from urls import ORDER_URL


@allure.feature("Order API")
@allure.story("Get orders for unauthorized user")
@allure.title("Test getting orders for unauthorized user")
def test_get_orders_unauthorized():
    """Тест получения заказов для неавторизованного пользователя."""
    url = ORDER_URL
    headers = {}  # Не передаем токен авторизации

    with allure.step("Send request to get orders without authorization"):
        response = requests.get(url, headers=headers)

    with allure.step("Validate response status and message"):
        # Проверяем, что статус ответа 401 (Unauthorized)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

        # Проверяем, что в ответе содержится ожидаемое сообщение об ошибке
        response_json = response.json()
        assert response_json.get("message") == "You should be authorised", (
            f"Expected 'You should be authorised', got '{response_json.get('message')}'"
        )

        # Прикрепляем тело ответа для отладки
        allure.attach(str(response_json), name="Response Body", attachment_type=allure.attachment_type.JSON)
