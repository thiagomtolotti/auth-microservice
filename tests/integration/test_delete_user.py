from starlette.testclient import TestClient

from tests.integration.constants import TEST_EMAIL, TEST_PASSWORD

from .flows import register_and_login, delete_user


def test_delete_user(client: TestClient):
    login = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    access_token = login.json()["access_token"]

    response = delete_user(client, access_token)

    assert response.status_code == 200


def test_delete_user_invalid_token(client: TestClient):
    response = delete_user(client, "invalid_token")

    assert response.status_code == 401


def test_delete_user_nonexistent_user(client: TestClient):
    # Create a valid token for a user that doesn't exist
    login = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    access_token = login.json()["access_token"]

    # Delete the user first
    delete_user(client, access_token)

    # Try to delete again with the same token
    response = delete_user(client, access_token)

    assert response.status_code == 400
