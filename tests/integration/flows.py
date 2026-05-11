from starlette.testclient import TestClient
from httpx import Response


def create_user(client: TestClient, email: str, password: str) -> Response:
    return client.post("/users/", json={"email": email, "password": password})


def login(client: TestClient, email: str, password: str) -> Response:
    return client.post("/users/login", json={"email": email, "password": password})


# TODO: add default email and password values to avoid having to pass them in every test that needs to register and login a user
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


def delete_user(client: TestClient, token: str) -> Response:
    return client.delete(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
    )


def forgot_password(client: TestClient, email: str) -> Response:
    return client.post(
        "/users/forgot_password",
        json={"email": email},
    )


def reset_password(
    client: TestClient, email: str, token: str, new_password: str
) -> Response:
    return client.post(
        "/users/reset_password",
        json={"email": email, "token": token, "new_password": new_password},
    )
