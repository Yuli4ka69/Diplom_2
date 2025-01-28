import allure
from faker import Faker

fake = Faker()

@allure.feature("User API")
@allure.story("Login existing user")
@allure.title("Test login for an existing user")
def test_login_existing_user(create_user, login_user):
    """Тест логина существующего пользователя."""

    # Генерация данных
    email = fake.email()  # Генерируется уникальный email
    password = "password123"

    with allure.step("Create a new user before login"):
        # Создание пользователя перед логином
        create_user(email=email, password=password, name="Test User")

    with allure.step("Login with the created user"):
        # Логинимся под этим пользователем
        response_data = login_user(email, password)  # login_user возвращает dict

    with allure.step("Validate login response"):
        # Проверяем успешный логин
        assert response_data.get('success') is True, "Login failed, expected 'success' to be True"
        assert "accessToken" in response_data, "Login response does not contain accessToken"

    # Прикрепляем тело ответа для диагностики
    allure.attach(str(response_data), name="Login Response Body", attachment_type=allure.attachment_type.JSON)

@allure.feature('User Management')
@allure.story('User Deletion')
@allure.title('Test user deletion')
def test_user_deletion(delete_user):
    """Тест для удаления пользователя."""
    # Фикстура автоматически удалит пользователя перед выполнением теста
    with allure.step("Delete user"):
        print(f"User deleted successfully: {delete_user.status_code}")
    assert delete_user.status_code == 202, f"Expected status 202, but got {delete_user.status_code}"
