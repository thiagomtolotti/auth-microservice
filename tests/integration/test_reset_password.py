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
