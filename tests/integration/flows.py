from starlette.testclient import TestClient
from httpx import Response

from .routes import Routes
from tests.integration.constants import TEST_EMAIL, TEST_PASSWORD


def get_route(route: Routes) -> str:
    return f"/auth{route.value}"


def create_user(client: TestClient, email: str, password: str) -> Response:
    return client.post(
        get_route(Routes.REGISTER), json={"email": email, "password": password}
    )


def login(client: TestClient, email: str, password: str) -> Response:
    return client.post(
        get_route(Routes.LOGIN), json={"email": email, "password": password}
    )


# TODO: add default email and password values to avoid having to pass them in every test that needs to register and login a user
def register_and_login(
    client: TestClient, email: str = TEST_EMAIL, password: str = TEST_PASSWORD
) -> Response:
    create_user(client, email, password)

    return login(client, email, password)


def logout(client: TestClient, token: str) -> Response:
    return client.post(
        get_route(Routes.LOGOUT), headers={"Authorization": f"Bearer {token}"}
    )


def access_protected(client: TestClient, token: str) -> Response:
    return client.get(
        get_route(Routes.PROTECTED), headers={"Authorization": f"Bearer {token}"}
    )


def refresh_token(
    client: TestClient, refresh_token: str, access_token: str
) -> Response:
    return client.post(
        get_route(Routes.REFRESH_TOKEN),
        headers={"Authorization": f"Bearer {access_token}"},
        json={"refresh_token": refresh_token},
    )


def change_password(client: TestClient, token: str, new_password: str) -> Response:
    return client.post(
        get_route(Routes.CHANGE_PASSWORD),
        headers={"Authorization": f"Bearer {token}"},
        json={"new_password": new_password},
    )


def delete_user(client: TestClient, token: str) -> Response:
    return client.delete(
        get_route(Routes.DELETE_USER),
        headers={"Authorization": f"Bearer {token}"},
    )


def forgot_password(client: TestClient, email: str) -> Response:
    return client.post(
        get_route(Routes.FORGOT_PASSWORD),
        json={"email": email},
    )


def reset_password(
    client: TestClient, email: str, token: str, new_password: str
) -> Response:
    return client.post(
        get_route(Routes.RESET_PASSWORD),
        json={"email": email, "token": token, "new_password": new_password},
    )
