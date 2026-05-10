from starlette.testclient import TestClient

from .flows import register_and_login, logout
from .constants import TEST_EMAIL, TEST_PASSWORD


def test_logout(client: TestClient):
    response = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)
    json = response.json()

    token = json.get("access_token")

    res = logout(client, token)

    print(res.json())

    assert res.status_code == 200
    assert res.json() == {"message": "Successfully logged out"}


def test_logout_with_invalid_token(client: TestClient):
    res = logout(client, "")

    print(res.json())

    assert res.status_code == 401
    assert res.json() == {"detail": "Invalid token"}
