from fastapi.testclient import TestClient
import pytest

from .constants import TEST_EMAIL, TEST_PASSWORD

from .flows import register_and_login


def test_ping(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200


def test_protected(client: TestClient):
    response = client.get("/protected")

    assert response.status_code == 401


def test_protected_with_token(client: TestClient):
    login = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    json = login.json()
    access_token = json["access_token"]

    response = client.get(
        "/protected", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_protected_with_invalid_token(client: TestClient):
    response = client.get(
        "/protected", headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401


def test_protected_with_expired_token(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr("app.domain.vos.tokens.ACCESS_TOKEN_DURATION", -1)

    login = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)
    json = login.json()
    access_token = json["access_token"]

    response = client.get(
        "/protected", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 401
