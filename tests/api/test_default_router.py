from unittest.mock import MagicMock, patch

from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
import pytest

from .api import DefaultRouter
from .routes import Routes


@pytest.fixture
def client():
    default_router = DefaultRouter()

    app = FastAPI()
    app.include_router(default_router.router)

    return TestClient(app)


@pytest.fixture()
def mock_token_decode():
    with patch("app.domain.vos.Token.decode") as mock:
        yield mock


def test_ping(client: TestClient):
    response = client.get(Routes.PING.value)

    assert response.status_code == 200
    assert response.json() == {"message": "Service is alive"}


def test_protected_route_without_token(client: TestClient):
    response = client.get(Routes.PROTECTED.value)

    assert response.status_code == 401
    assert response.json() == {"message": "Authorization header missing"}


def test_protected_route_with_invalid_token(
    client: TestClient, mock_token_decode: MagicMock
):
    mock_token_decode.side_effect = Exception("Invalid token")

    response = client.get(
        Routes.PROTECTED.value, headers={"Authorization": "Bearer invalidtoken"}
    )

    assert response.status_code == 401
    assert response.json() == {"message": "Invalid token"}


def test_protected_route_with_valid_token(
    client: TestClient, mock_token_decode: MagicMock
):
    mock_token_decode.return_value = {"user_id": "123"}

    response = client.get(
        Routes.PROTECTED.value, headers={"Authorization": "Bearer validtoken"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "This is a protected route"}
