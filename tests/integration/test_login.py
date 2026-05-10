from starlette.testclient import TestClient

from .constants import TEST_EMAIL, TEST_PASSWORD
from .flows import create_user, login


def test_login(client: TestClient):

    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    response = login(client, TEST_EMAIL, TEST_PASSWORD)

    assert response.status_code == 200

    json_response = response.json()

    assert "access_token" in json_response
    assert "refresh_token" in json_response


def test_no_user_login(client: TestClient):
    response = login(client, TEST_EMAIL, TEST_PASSWORD)

    assert response.status_code == 400

    json_response = response.json()

    assert json_response["type"] == "LoginFailedException"
    assert json_response["detail"] == "Invalid email or password"


def test_wrong_password_login(client: TestClient):

    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    response = login(client, TEST_EMAIL, "wrong_password")

    assert response.status_code == 400

    json_response = response.json()

    assert json_response["type"] == "LoginFailedException"
    assert json_response["detail"] == "Invalid email or password"
