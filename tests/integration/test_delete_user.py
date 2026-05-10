from starlette.testclient import TestClient

from tests.integration.constants import TEST_EMAIL, TEST_PASSWORD

from .flows import register_and_login, delete_user


def test_delete_user(client: TestClient):
    login = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    access_token = login.json()["access_token"]

    response = delete_user(client, access_token)

    assert response.status_code == 200
