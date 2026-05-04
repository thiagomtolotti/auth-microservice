from unittest.mock import MagicMock

from fastapi.applications import FastAPI
from fastapi.testclient import TestClient
import pytest

from app.api.default_router import DefaultRouter
from app.domain.vos import Token


@pytest.fixture
def client():
    default_router = DefaultRouter()

    app = FastAPI()
    app.include_router(default_router.router)

    return TestClient(app)


def test_ping(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Service is alive"}


def test_protected_route_without_token(client: TestClient):
    response = client.get("/protected")

    assert response.status_code == 401
    assert response.json() == {"message": "Authorization header missing"}


def test_protected_route_with_invalid_token(client: TestClient):
    Token.decode = MagicMock(side_effect=Exception("Invalid token"))

    response = client.get(
        "/protected", headers={"Authorization": "Bearer invalidtoken"}
    )

    assert response.status_code == 401
    assert response.json() == {"message": "Invalid token"}


def test_protected_route_with_valid_token(client: TestClient):
    Token.decode = MagicMock(return_value={"user_id": "123"})

    response = client.get("/protected", headers={"Authorization": "Bearer validtoken"})

    assert response.status_code == 200
    assert response.json() == {"message": "This is a protected route"}
