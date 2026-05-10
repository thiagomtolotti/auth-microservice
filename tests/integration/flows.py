from starlette.testclient import TestClient
from httpx import Response


def create_user(client: TestClient, email: str, password: str) -> Response:
    return client.post("/users/", json={"email": email, "password": password})


def login(client: TestClient, email: str, password: str) -> Response:
    return client.post("/users/login", json={"email": email, "password": password})


def register_and_login(client: TestClient, email: str, password: str) -> Response:
    create_user(client, email, password)

    return login(client, email, password)


def logout(client: TestClient, token: str) -> Response:
    return client.post("/users/logout", headers={"Authorization": f"Bearer {token}"})
