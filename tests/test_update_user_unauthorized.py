import pytest
from faker import Faker
import allure


fake = Faker()

@pytest.mark.parametrize("field, new_value", [
    ("name", fake.name()),
    ("email", fake.email()),
    ("password", fake.password())
])
@allure.feature("User API")
@allure.story("Update user details")
@allure.title("Test update user details without authorization")
def test_update_user_without_authorization(update_user, field, new_value):
    """Тест обновления данных для неавторизованного пользователя."""

    # Попытка обновить данные без токена
    with allure.step(f"Attempt to update user {field} with new value: {new_value} without authorization"):
        update_response = update_user(field=field, new_value=new_value)  # токен не передаем

        allure.attach(f"Response status code: {update_response['status_code']}", name="Response Status Code", attachment_type=allure.attachment_type.TEXT)
        assert update_response["status_code"] == 401, f"Expected 401, got {update_response['status_code']}"

        # Проверка правильности сообщения об ошибке
        assert update_response["message"] == "You should be authorised", f"Expected 'You should be authorised', got {update_response['message']}"

@allure.feature('User Management')
@allure.story('User Deletion')
@allure.title('Test user deletion')
def test_user_deletion(delete_user):
    """Тест для удаления пользователя."""
    # Фикстура автоматически удалит пользователя перед выполнением теста
    with allure.step("Delete user"):
        print(f"User deleted successfully: {delete_user.status_code}")
    assert delete_user.status_code == 202, f"Expected status 202, but got {delete_user.status_code}"
