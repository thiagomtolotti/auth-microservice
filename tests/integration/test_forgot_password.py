from starlette.testclient import TestClient

from tests.integration.constants import TEST_EMAIL, TEST_PASSWORD

from .flows import create_user


def test_forgot_password(client: TestClient):
    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    forgot_password_res = client.post(
        "/users/forgot_password",
        json={"email": TEST_EMAIL},
    )

    assert forgot_password_res.status_code == 200
