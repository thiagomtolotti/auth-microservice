from starlette.testclient import TestClient

from app.main import app

from .constants import TEST_EMAIL, TEST_PASSWORD
from .flows import create_user, login


def test_login():
    client = TestClient(app)

    create_user(client, TEST_EMAIL, TEST_PASSWORD)

    response = login(client, TEST_EMAIL, TEST_PASSWORD)

    assert response.status_code == 200

    json_response = response.json()

    assert "access_token" in json_response
    assert "refresh_token" in json_response
