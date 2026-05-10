import pytest
from starlette.testclient import TestClient

from tests.integration.constants import TEST_EMAIL, TEST_PASSWORD

from .flows import register_and_login, access_protected, refresh_token


def test_refresh_token(client: TestClient, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("app.domain.vos.tokens.ACCESS_TOKEN_DURATION", -1)

    login = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    json = login.json()

    access_token_str = json["access_token"]
    refresh_token_str = json["refresh_token"]

    response = access_protected(client, access_token_str)

    assert response.status_code == 401

    monkeypatch.setattr("app.domain.vos.tokens.ACCESS_TOKEN_DURATION", 5)

    response = refresh_token(client, refresh_token_str, access_token_str)

    assert response.status_code == 200

    json = response.json()

    new_access_token_str = json["access_token"]

    response = access_protected(client, new_access_token_str)

    assert response.status_code == 200


def test_refresh_token_with_invalid_token(client: TestClient):
    response = refresh_token(client, "invalid_refresh_token", "invalid_access_token")

    assert response.status_code == 401


def test_refresh_token_with_expired_refresh_token(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr("app.domain.vos.tokens.REFRESH_TOKEN_DURATION", -1)

    login = register_and_login(client, TEST_EMAIL, TEST_PASSWORD)

    json = login.json()

    access_token_str = json["access_token"]
    refresh_token_str = json["refresh_token"]

    response = refresh_token(client, refresh_token_str, access_token_str)

    assert response.status_code == 401
