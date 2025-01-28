import pytest
from faker import Faker
import allure

fake = Faker()

@pytest.mark.parametrize(
    "email, password, name, expected_status_code, expected_message",
    [
        (None, fake.password(), fake.user_name(), 403, "Email, password and name are required fields"),
        (fake.email(), None, fake.user_name(), 403, "Email, password and name are required fields"),
        (fake.email(), fake.password(), None, 403, "Email, password and name are required fields"),
    ]
)
@allure.feature('User Management')
@allure.story('User Registration')
@allure.title('Test user registration with missing fields')
def test_create_user_with_missing_fields(create_user_with_missing_fields_error, email, password, name, expected_status_code, expected_message):
    """Тест создания пользователя без обязательных полей."""

    with allure.step(f"Attempt to register user with email={email}, password={password}, name={name}"):
        response, message, email, password = create_user_with_missing_fields_error(email, password, name)
    with allure.step(f"Check response status code"):
        assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code}"
    with allure.step(f"Check response message"):
        assert message == expected_message, f"Expected message '{expected_message}', but got '{message}'"

@allure.feature('User Management')
@allure.story('User Deletion')
@allure.title('Test user deletion')
def test_user_deletion(delete_user):
    """Тест для удаления пользователя."""
    with allure.step("Delete user"):
        print(f"User deleted successfully: {delete_user.status_code}")
    with allure.step(f"Check response status code"):
        assert delete_user.status_code == 202, f"Expected status 202, but got {delete_user.status_code}"