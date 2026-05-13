import pytest

from fastapi.testclient import TestClient

from app.routes import Routes

from .flows import get_route, register_and_login, delete_user, access_protected



def test_ping(client: TestClient):
    response = client.get(get_route(Routes.PING))

    assert response.status_code == 200


def test_protected(client: TestClient):
    response = client.get(get_route(Routes.PROTECTED))

    assert response.status_code == 401


def test_protected_with_token(client: TestClient):
    login = register_and_login(client)

    json = login.json()
    access_token = json["access_token"]

    response = access_protected(client, access_token)
    assert response.status_code == 200


def test_protected_with_invalid_token(client: TestClient):
    response = access_protected(client, "invalid_token")

    assert response.status_code == 401


def test_protected_with_expired_token(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr("app.domain.vos.tokens.ACCESS_TOKEN_DURATION", -1)

    login = register_and_login(client)
    json = login.json()
    access_token = json["access_token"]

    response = access_protected(client, access_token)

    assert response.status_code == 401


def test_protected_refresh_token(client: TestClient):
    login = register_and_login(client)
    json = login.json()
    refresh_token = json["refresh_token"]

    response = client.get(
        get_route(Routes.PROTECTED),
        headers={"Authorization": f"Bearer {refresh_token}"},
    )

    assert response.status_code == 401


def test_protected_deleted_user(client: TestClient):
    login = register_and_login(client)
    json = login.json()
    access_token = json["access_token"]
    

    delete_user(client, access_token)

    response = access_protected(client, access_token)

    assert response.status_code == 400
