import pytest
import requests
from urls import ORDER_URL
import allure

@allure.feature("Order API")
@allure.story("Create order without authorization")
@allure.title("Test create order without authorization")
@pytest.mark.parametrize("ingredients, expected_status, expected_message", [
    (["61c0c5a71d1f82001bdaaa7a", "61c0c5a71d1f82001bdaaa78"], 200, None),
    ([], 400, "Ingredient ids must be provided"),
    (["61c0c5a71d1f82001bdaaa7a", "123321"], 500, "Ingredient not found"),
])
def test_create_order_without_authorization(ingredients, expected_status, expected_message):
    """Тест создания заказов для неавторизованного пользователя."""
    with allure.step(f"Attempt to create order without authorization with ingredients={ingredients}"):
        headers = {"Authorization": ""}  # Пустой токен для проверки неавторизованного запроса
        response = requests.post(ORDER_URL, json={"ingredients": ingredients}, headers=headers)

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