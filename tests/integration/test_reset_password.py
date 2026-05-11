import pytest
from starlette.testclient import TestClient

from tests.integration.constants import TEST_EMAIL, TEST_PASSWORD
from tests.integration.fixtures import MockNotificationHandler
from .flows import create_user, forgot_password, reset_password


def test_reset_password(
    client: TestClient, notification_handler: MockNotificationHandler
):
    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    forgot_password(client, TEST_EMAIL)

    token = notification_handler.forgot_password_calls[0].token

    reset_password_res = reset_password(client, TEST_EMAIL, token, "@newpassword123")

    assert reset_password_res.status_code == 200


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
