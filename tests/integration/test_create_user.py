from fastapi.testclient import TestClient

from app.api.main import Routes
from app.domain.exceptions import UserAlreadyExistsException

from .flows import create_user, get_route
from .constants import TEST_EMAIL, TEST_PASSWORD


def test_create_user(client: TestClient):
    response = create_user(client, TEST_EMAIL, TEST_PASSWORD)

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_create_duplicate_user(client: TestClient):
    # Create the user for the first time
    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    # Try to create the same user again
    response = create_user(client, TEST_EMAIL, TEST_PASSWORD)

    assert response.status_code == 400

    json_response = response.json()

    assert json_response["type"] == UserAlreadyExistsException.__name__
    assert json_response["detail"] == "User already exists"


def test_create_user_invalid_email(client: TestClient):
    invalid_email = "invalid-email"

    response = create_user(client, invalid_email, TEST_PASSWORD)

    assert response.status_code == 422

    json_response = response.json()

    assert json_response["type"] == "ValidationError"


def test_create_user_short_password(client: TestClient):
    invalid_password = "short"

    response = create_user(client, TEST_EMAIL, invalid_password)

    assert response.status_code == 422

    json_response = response.json()

    assert json_response["type"] == "ValidationError"


def test_create_user_missing_fields(client: TestClient):
    response = client.post(get_route(Routes.REGISTER), json={})

    assert response.status_code == 422

    json_response = response.json()

    assert json_response["type"] == "ValidationError"
