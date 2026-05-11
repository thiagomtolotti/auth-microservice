from starlette.testclient import TestClient

from tests.integration.constants import TEST_EMAIL, TEST_PASSWORD
from tests.integration.fixtures import MockNotificationHandler

from .flows import create_user, forgot_password


def test_forgot_password(
    client: TestClient, notification_handler: MockNotificationHandler
):
    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    forgot_password_res = forgot_password(client, TEST_EMAIL)

    assert forgot_password_res.status_code == 200

    assert len(notification_handler.forgot_password_calls) == 1
    assert notification_handler.forgot_password_calls[0].email == TEST_EMAIL


def test_forgot_password_non_existent_email(
    client: TestClient, notification_handler: MockNotificationHandler
):
    from app.dependencies import get_users_repo

    forgot_password_res = forgot_password(client, "nonexistent@example.com")

    repo = get_users_repo()

    assert forgot_password_res.status_code == 200

    assert len(repo.forgot_password_tokens) == 0
    assert len(notification_handler.forgot_password_calls) == 0


def test_forgot_password_invalid_email(client: TestClient):
    forgot_password_res = forgot_password(client, "invalid-email")

    assert forgot_password_res.status_code == 422
