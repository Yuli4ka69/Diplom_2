import pytest
from faker import Faker
import allure

fake = Faker()

@allure.feature('User Registration')
@allure.story('Create Duplicate User')
@allure.title('Test creating duplicate user')
def test_create_duplicate_user(create_user_with_error_handling):
    """Тест на создание дублирующего пользователя."""
    # Данные для пользователя
    email = fake.email()
    password = fake.password()
    name = fake.name()

    # Шаг 1: Создаем первого пользователя
    with allure.step("Create first user"):
        response, error_message, created_email, created_password = create_user_with_error_handling(email=email,
                                                                                                   password=password,
                                                                                                   name=name)

    # Проверяем, что регистрация прошла успешно (для первого пользователя)
    assert response.status_code == 200, f"Expected status 200, but got {response.status_code}"
    allure.attach(f"User created with email: {created_email}", name="User Created Info", attachment_type=allure.attachment_type.TEXT)

    # Шаг 2: Попытка создать дублирующего пользователя
    with allure.step("Try to create duplicate user"):
        response, error_message, _, _ = create_user_with_error_handling(email=email, password=password, name=name)

    # Проверяем, что повторная регистрация приводит к ошибке 403 с правильным сообщением
    assert response.status_code == 403, f"Expected status 403, but got {response.status_code}"
    assert error_message == "User already exists", f"Expected error message 'User already exists', but got {error_message}"


@allure.feature('User Management')
@allure.story('User Deletion')
@allure.title('Test user deletion')
def test_user_deletion(delete_user):
    """Тест для удаления пользователя."""
    # Фикстура автоматически удалит пользователя перед выполнением теста
    with allure.step("Delete user"):
        print(f"User deleted successfully: {delete_user.status_code}")
    assert delete_user.status_code == 202, f"Expected status 202, but got {delete_user.status_code}"
