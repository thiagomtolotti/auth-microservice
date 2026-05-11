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


def test_forgot_password_non_existent_email(client: TestClient):
    from app.dependencies import get_users_repo

    forgot_password_res = client.post(
        "/users/forgot_password",
        json={"email": "nonexistent@example.com"},
    )

    repo = get_users_repo()

    assert len(repo.forgot_password_tokens) == 0
    assert forgot_password_res.status_code == 200


def test_forgot_password_invalid_email(client: TestClient):
    forgot_password_res = client.post(
        "/users/forgot_password",
        json={"email": "invalid-email"},
    )

    assert forgot_password_res.status_code == 422
