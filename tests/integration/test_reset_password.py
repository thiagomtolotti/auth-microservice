import pytest
from starlette.testclient import TestClient

from .constants import TEST_EMAIL, TEST_PASSWORD
from .fixtures import MockNotificationHandler
from .flows import create_user, forgot_password, reset_password, login


def test_reset_password(
    client: TestClient, notification_handler: MockNotificationHandler
):
    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    forgot_password(client, TEST_EMAIL)

    token = notification_handler.forgot_password_calls[0].token

    NEW_PASSWORD = "@newpassword123"

    reset_password_res = reset_password(client, TEST_EMAIL, token, NEW_PASSWORD)

    assert reset_password_res.status_code == 200

    login_res = login(client, TEST_EMAIL, NEW_PASSWORD)

    assert login_res.status_code == 200


def test_reset_password_with_invalid_token(client: TestClient):
    reset_password_res = reset_password(
        client, TEST_EMAIL, "invalid-token", "@newpassword123"
    )

    assert reset_password_res.status_code == 400


def test_reset_password_with_expired_token(
    client: TestClient,
    notification_handler: MockNotificationHandler,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr("app.services.users.FORGOT_PASSWORD_TOKEN_DURATION", -1)

    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    forgot_password(client, TEST_EMAIL)

    token = notification_handler.forgot_password_calls[0].token

    reset_password_res = reset_password(client, TEST_EMAIL, token, "@newpassword123")

    assert reset_password_res.status_code == 422


def test_reset_password_with_same_password(
    client: TestClient, notification_handler: MockNotificationHandler
):
    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    forgot_password(client, TEST_EMAIL)

    token = notification_handler.forgot_password_calls[0].token

    reset_password_res = reset_password(client, TEST_EMAIL, token, TEST_PASSWORD)

    assert reset_password_res.status_code == 422


def test_reset_password_with_nonexistent_email(client: TestClient):
    reset_password_res = reset_password(
        client, "nonexistent@example.com", "any-token", "@newpassword123"
    )

    json = reset_password_res.json()

    assert reset_password_res.status_code == 400

    assert json["type"] == "UserNotFoundException"
    assert json["detail"] == "User not found"
