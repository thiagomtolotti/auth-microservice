from app.domain.vos.password import Password

from app.domain.models.user import UserModel

import pytest


@pytest.fixture
def test_user():
    email = "test@example.com"
    password = Password("@aa123456")

    return UserModel(email=email, password=password)


def test_user_creation(test_user: UserModel):
    assert test_user.email == "test@example.com"
    assert test_user.password is not None
    assert test_user.id is not None


def test_user_login(test_user: UserModel):
    login_response = test_user.login()

    assert login_response.access_token is not None
    assert login_response.refresh_token is not None
    assert login_response.created_at is not None
    assert login_response.refresh_expires_at is not None
    assert login_response.jti is not None


def test_refresh_access_token(test_user: UserModel):
    access_token = test_user.refresh_access_token()

    assert access_token is not None
