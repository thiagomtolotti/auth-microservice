from starlette.testclient import TestClient

from .constants import TEST_EMAIL, TEST_PASSWORD

from .flows import register_and_login, change_password, logout, login


def test_change_password(client: TestClient):
    login_res = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    json = login_res.json()

    access_token = json["access_token"]

    new_password = "@newpassword123"

    response = change_password(client, access_token, new_password)

    assert response.status_code == 200

    logout(client, access_token)

    login_res = login(client, TEST_EMAIL, TEST_PASSWORD)

    print(login_res.json())

    assert login_res.status_code == 400

    login_res = login(client, TEST_EMAIL, new_password)

    assert login_res.status_code == 200


def test_change_password_unauthorized(client: TestClient):
    response = change_password(client, "invalid_token", "@newpassword123")

    assert response.status_code == 401


def test_change_password_invalid_input(client: TestClient):
    login_res = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    json = login_res.json()

    access_token = json["access_token"]

    response = change_password(client, access_token, "")
    assert response.status_code == 422

    response = change_password(client, access_token, "@short1")
    assert response.status_code == 422

    response = change_password(client, access_token, "@nonumbers")
    assert response.status_code == 422

    response = change_password(client, access_token, "nospecialchars123")
    assert response.status_code == 422


def test_change_password_same_as_old(client: TestClient):
    login_res = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    json = login_res.json()

    access_token = json["access_token"]

    response = change_password(client, access_token, TEST_PASSWORD)

    assert response.status_code == 422
