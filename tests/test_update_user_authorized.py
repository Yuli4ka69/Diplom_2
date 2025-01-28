import pytest
import allure
import requests
from conftest import create_user, login_user, update_user, auth_token
from faker import Faker
from urls import UPDATE_USER_URL

fake = Faker()

@pytest.mark.parametrize(
    "field, new_value",
    [
        ("name", fake.name()),
        ("email", f"{fake.email()}_{fake.uuid4()}"),
        ("password", "newpassword"),
    ]
)
@allure.feature("User API")
@allure.story("Update user information with authorization")
@allure.title("Test updating user information with authorization")
def test_update_user(create_user, login_user, update_user, auth_token, field, new_value):
    """Тест обновления данных для авторизованного пользователя."""
    email = f"{fake.email()}_{fake.uuid4()}"
    password = "password"

    # Регистрация пользователя
    register_response, register_data, email, password = create_user(email=email, password=password)
    assert register_response.status_code in [200, 201], f"Registration failed with status code {register_response.status_code}"

    # Авторизация (вместо повторной авторизации используем токен из фикстуры)
    auth_token = auth_token  # Используем токен, полученный из фикстуры

    # Обновление данных пользователя
    update_data = {
        field: new_value  # передаем изменённое поле и значение
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    # Отправка запроса PATCH
    update_response = requests.patch(UPDATE_USER_URL, json=update_data, headers=headers)

    # Выводим информацию о статусе и тексте ответа
    print(f"Response Status Code: {update_response.status_code}")
    print(f"Response Text: {update_response.text}")

    # Явная проверка успешности выполнения запроса
    assert update_response.status_code == 200, f"Update failed with status code {update_response.status_code}"

@allure.feature('User Management')
@allure.story('User Deletion')
@allure.title('Test user deletion')
def test_user_deletion(delete_user):
    """Тест для удаления пользователя."""
    # Фикстура автоматически удалит пользователя
    with allure.step("Delete user"):
        print(f"User deleted successfully: {delete_user.status_code}")
    assert delete_user.status_code == 202, f"Expected status 202, but got {delete_user.status_code}"
