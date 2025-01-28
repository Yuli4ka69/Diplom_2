from faker import Faker
import allure

fake = Faker()

@allure.feature("User API")
@allure.story("Create unique user")
@allure.title("Test create unique user")
def test_create_unique_user(create_user):
    """Тест создания уникального пользователя."""

    email = fake.email()
    password = fake.password()
    name = fake.name()

    # Создаем уникального пользователя
    response, response_data, created_email, created_password = create_user(email=email, password=password, name=name)

    # Вывод для диагностики
    print(response_data)

    # Проверяем успешное создание пользователя
    assert response_data["status_code"] == 200

@allure.feature('User Management')
@allure.story('User Deletion')
@allure.title('Test user deletion')
def test_user_deletion(delete_user):
    """Тест для удаления пользователя."""
    # Фикстура автоматически удалит пользователя перед выполнением теста
    with allure.step("Delete user"):
        print(f"User deleted successfully: {delete_user.status_code}")
    assert delete_user.status_code == 202, f"Expected status 202, but got {delete_user.status_code}"
