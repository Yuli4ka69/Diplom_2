import allure
import pytest
from conftest import create_user
from faker import Faker
import requests
from urls import USER_LOGIN_URL


fake = Faker()

@allure.feature("User API")
@allure.story("Login with invalid credentials")
@allure.title("Test login with invalid credentials")
@pytest.mark.parametrize(
    "email, password, expected_error_message",
    [
        (fake.email(), "wrongpassword", "email or password are incorrect"),
        ("wrongemail@yandex.ru", fake.password(), "email or password are incorrect")
    ]
)
def test_login_invalid_credentials(create_user, email, password, expected_error_message):
    """Тест логина с неправильными данными."""

    # Генерация данных для нового пользователя
    user_email = f"{fake.email().split('@')[0]}_{fake.random_number()}@example.com"
    user_password = fake.password()
    name = fake.name()

    with allure.step("Create a user with valid credentials"):
        # Создаем пользователя с правильными данными
        create_user(email=user_email, password=user_password, name=name)

    with allure.step(f"Attempt to login with email: {email} and password: {password}"):
        # Попытка логина с неправильными данными
        response = requests.post(USER_LOGIN_URL, json={
            "email": email,
            "password": password
        })

    with allure.step("Validate login response for invalid credentials"):
        # Проверяем статус и сообщение об ошибке
        assert response.status_code == 401, f"Unexpected status code: {response.status_code}"
        response_data = response.json()
        assert response_data.get("message") == expected_error_message, (
            f"Unexpected error message: {response_data.get('message')}"
        )
