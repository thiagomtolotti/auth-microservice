from fastapi.testclient import TestClient

from app.main import app
from app.domain.exceptions import UserAlreadyExistsException

from .flows import create_user
from .constants import TEST_EMAIL, TEST_PASSWORD


def test_create_user():
    client = TestClient(app)

    response = create_user(client, TEST_EMAIL, TEST_PASSWORD)

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_create_duplicate_user():
    client = TestClient(app)

    # Create the user for the first time
    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    # Try to create the same user again
    response = create_user(client, TEST_EMAIL, TEST_PASSWORD)

    assert response.status_code == 400

    json_response = response.json()

    assert json_response["type"] == UserAlreadyExistsException.__name__
    assert json_response["detail"] == "User already exists"


def test_create_user_invalid_email():
    client = TestClient(app)

    invalid_email = "invalid-email"

    response = create_user(client, invalid_email, TEST_PASSWORD)

    assert response.status_code == 422

    json_response = response.json()

    assert json_response["type"] == "ValidationError"


def test_create_user_short_password():
    client = TestClient(app)

    invalid_password = "short"

    response = create_user(client, TEST_EMAIL, invalid_password)

    assert response.status_code == 422

    json_response = response.json()

    assert json_response["type"] == "ValidationError"


def test_create_user_missing_fields():
    client = TestClient(app)

    response = client.post("/users/", json={})

    assert response.status_code == 422

    json_response = response.json()

    assert json_response["type"] == "ValidationError"
