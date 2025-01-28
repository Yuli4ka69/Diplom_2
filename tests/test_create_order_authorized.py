import pytest
import allure
from conftest import create_order, auth_token


@pytest.mark.parametrize("ingredients, expected_status, expected_message", [
    (["61c0c5a71d1f82001bdaaa7a", "61c0c5a71d1f82001bdaaa78"], 200, None),  # С ингредиентами, успешный ответ
    ([], 400, "Ingredient ids must be provided"),  # Пустой список ингредиентов, ошибка 400
    (["61c0c5a71d1f82001bdaaa7a", "123321"], 500, "Internal Server Error"),  # Неверный ингредиент, ошибка 500
])
@allure.feature("Order API")
@allure.story("Create order with authorization")
@allure.title("Test creating order with authorization")
def test_create_order_with_authorization(auth_token, create_order, ingredients, expected_status, expected_message):
    """Тест создания заказов для авторизованного пользователя."""
    with allure.step(f"Attempt to create order with ingredients={ingredients}"):
        response = create_order(ingredients)

    with allure.step(f"Check response status code"):
        assert response.status_code == expected_status, f"Unexpected status code: {response.status_code}, {response.text}"

    with allure.step(f"Check response message"):
        if expected_status == 500:
            assert "Internal Server Error" in response.text, f"Expected 'Internal Server Error', but got: {response.text}"
        elif expected_message:
            try:
                response_json = response.json()
                assert response_json.get(
                    "message") == expected_message, f"Unexpected message: {response_json.get('message')}"
            except ValueError:  # В случае ошибки при декодировании JSON, выведем ответ как текст
                assert expected_message in response.text, f"Expected message '{expected_message}', but got: {response.text}"