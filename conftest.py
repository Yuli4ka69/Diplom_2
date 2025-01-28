import pytest
import requests
from faker import Faker
from urls import ORDER_URL, USER_REGISTER_URL, USER_LOGIN_URL, UPDATE_USER_URL, USER_DELETE_URL

fake = Faker()

@pytest.fixture
def create_user():
    """Создает пользователя и возвращает данные пользователя, объект ответа и токен, если есть."""
    def _create_user(email=None, password=None, name=None):
        email = email or fake.email()
        password = password or fake.password()
        name = name or fake.name()
        response = requests.post(USER_REGISTER_URL, json={
            "email": email,
            "password": password,
            "name": name
        })
        assert response.status_code == 200, f"Error during user registration: {response.status_code}, {response.text}"
        response_data = response.json()
        response_data["status_code"] = response.status_code
        if "accessToken" in response_data:
            response_data["accessToken"] = response_data["accessToken"]
        return response, response_data, email, password
    return _create_user


@pytest.fixture
def create_user_with_error_handling(create_user):
    """Фикстура для создания пользователя с обработкой ошибок, включая создание дубля."""

    def _create_user_with_error_handling(email=None, password=None, name=None):
        email = email or fake.email()
        password = password or fake.password()
        name = name or fake.name()

        # Попытка регистрации пользователя
        response = requests.post(USER_REGISTER_URL, json={
            "email": email,
            "password": password,
            "name": name
        })

        if response.status_code == 403:  # Пользователь уже существует или отсутствуют обязательные поля
            response_json = response.json()
            if "Email, password and name are required fields" in response_json.get("message", ""):
                return response, "Email, password and name are required fields", email, password
            elif "User already exists" in response_json.get("message", ""):
                return response, "User already exists", email, password
        else:
            # Обработка других ошибок
            return response, response.text, email, password

    return _create_user_with_error_handling


@pytest.fixture
def auth_token(create_user, login_user):
    """Регистрирует пользователя, авторизует его и возвращает токен."""
    _, _, email, password = create_user()
    response_data = login_user(email, password)
    token = response_data.get("accessToken")
    assert token, "Access token is missing in response"
    return token.split()[-1]

@pytest.fixture
def create_order(auth_token):
    """Фикстура для создания заказа с использованием токена авторизации."""
    headers = {"Authorization": f"Bearer {auth_token}"}

    def _create_order(ingredients):
        response = requests.post(ORDER_URL, json={"ingredients": ingredients}, headers=headers)
        return response

    return _create_order


@pytest.fixture
def login_user():
    """Авторизует пользователя и возвращает данные авторизации."""
    def _login_user(email, password):
        response = requests.post(USER_LOGIN_URL, json={
            "email": email,
            "password": password
        })
        assert response.status_code == 200, f"Login failed: {response.status_code}, {response.text}"
        return response.json()

    return _login_user


@pytest.fixture
def update_user():
    """Фикстура для обновления данных пользователя."""

    def _update_user(field, new_value, token=None):
        if not token:
            return {"status_code": 401, "message": "You should be authorised"}

        headers = {"Authorization": f"Bearer {token}"}
        payload = {field: new_value}
        response = requests.patch(UPDATE_USER_URL, json=payload, headers=headers)

        print(f"Response: {response.status_code}, {response.text}")
        return response

    return _update_user


@pytest.fixture
def delete_user(auth_token):
    """Удаляет пользователя по токену после выполнения теста."""
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    # Отправляем запрос на удаление пользователя
    response = requests.delete(USER_DELETE_URL, headers=headers)

    # Проверяем, что удаление прошло успешно
    assert response.status_code == 202, f"Failed to delete user: {response.status_code}, {response.text}"

    return response

@pytest.fixture
def create_user_with_missing_fields_error():
    """Фикстура для создания пользователя с ошибкой, когда отсутствуют обязательные поля."""
    def _create_user_with_missing_fields_error(email=None, password=None, name=None):
        # Попытка регистрации пользователя с отсутствующими полями
        response = requests.post(USER_REGISTER_URL, json={
            "email": email,
            "password": password,
            "name": name
        })
        if response.status_code == 403:  # Пользователь уже существует или отсутствуют обязательные поля
            response_json = response.json()
            if "Email, password and name are required fields" in response_json.get("message", ""):
                return response, "Email, password and name are required fields", email, password
            elif "User already exists" in response_json.get("message", ""):
                return response, "User already exists", email, password
        else:
            # Обработка других ошибок
            return response, response.text, email, password
    return _create_user_with_missing_fields_error