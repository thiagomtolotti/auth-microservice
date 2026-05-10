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


def access_protected(client: TestClient, token: str) -> Response:
    return client.get("/protected", headers={"Authorization": f"Bearer {token}"})


def refresh_token(
    client: TestClient, refresh_token: str, access_token: str
) -> Response:
    return client.post(
        "/users/refresh",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token": refresh_token},
    )


def change_password(client: TestClient, token: str, new_password: str) -> Response:
    return client.post(
        "/users/change_password",
        headers={"Authorization": f"Bearer {token}"},
        json={"new_password": new_password},
    )
