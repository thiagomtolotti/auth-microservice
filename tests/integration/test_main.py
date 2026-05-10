from fastapi.testclient import TestClient
from app.domain.exceptions import UserAlreadyExistsException
from app.main import app

from .flows import create_user


def test_ping():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200


def test_create_user():
    client = TestClient(app)

    test_email = "test@example.com"
    test_password = "@password123"

    response = create_user(client, test_email, test_password)

    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_create_duplicate_user():
    client = TestClient(app)

    test_email = "test@example.com"
    test_password = "@password123"

    # Create the user for the first time
    create_user(client, test_email, test_password)

    # Try to create the same user again
    response = create_user(client, test_email, test_password)

    assert response.status_code == 400

    json_response = response.json()

    assert json_response["type"] == UserAlreadyExistsException.__name__
    assert json_response["detail"] == "User already exists"
