import datetime

from app.utils.types import CreateUserHandlerDTO, LoginHandlerDTO
from app.domain.vos import CreateTokenPayload, RefreshToken
from app.repositories.users import InMemoryUsersRepository
from app.services.users import UsersService

import pytest


@pytest.fixture
def service():
    return UsersService(repository=InMemoryUsersRepository())


@pytest.fixture()
def email():
    return "test@example.com"


@pytest.fixture()
def password():
    return "@aa123456"


def test_create_success(service: UsersService, email: str, password: str):

    service.create(CreateUserHandlerDTO(email=email, password=password))

    assert service.repository.find_by_email(email) is not None


def test_create_user_already_exists(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    with pytest.raises(Exception) as exc_info:
        service.create(CreateUserHandlerDTO(email=email, password=password))

    assert str(exc_info.value) == "User already exists"


def test_login_success(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    response = service.login(LoginHandlerDTO(email=email, password=password))

    assert response.access_token is not None
    assert response.refresh_token is not None


def test_login_invalid_email(service: UsersService, email: str, password: str):
    with pytest.raises(Exception) as exc_info:
        service.login(LoginHandlerDTO(email=email, password=password))

    assert str(exc_info.value) == "Invalid email or password"


def test_login_invalid_password(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    with pytest.raises(Exception) as exc_info:
        service.login(LoginHandlerDTO(email=email, password="wrongpassword"))

    assert str(exc_info.value) == "Invalid email or password"


def test_logout_success(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    service.login(LoginHandlerDTO(email=email, password=password))

    service.logout(email)

    assert service.repository.find_by_email(email) is not None


def test_logout_invalid_email(service: UsersService, email: str):
    with pytest.raises(Exception) as exc_info:
        service.logout(email)

    assert str(exc_info.value) == "Invalid email address"


def test_logout_failed(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    with pytest.raises(Exception) as exc_info:
        service.logout(email)

    assert str(exc_info.value) == "Failed to log out user"


def test_refresh_token_success(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    login_response = service.login(LoginHandlerDTO(email=email, password=password))

    new_access_token = service.refresh_token(login_response.refresh_token)

    assert new_access_token is not None


def test_refresh_token_invalid_token(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    invalid_token = RefreshToken(
        CreateTokenPayload(
            sub="invalid",
            duration=datetime.timedelta(seconds=100),
        )
    )

    with pytest.raises(Exception) as exc_info:
        service.refresh_token(invalid_token.get())

    assert str(exc_info.value) == "Invalid refresh token"


def test_refresh_token_expired_token(service: UsersService, email: str, password: str):
    service.create(CreateUserHandlerDTO(email=email, password=password))

    expired_token = RefreshToken(
        CreateTokenPayload(
            sub="invalid",
            duration=datetime.timedelta(seconds=-100),
        )
    )

    with pytest.raises(Exception) as exc_info:
        service.refresh_token(expired_token.get())

    assert str(exc_info.value) == "Signature has expired"
