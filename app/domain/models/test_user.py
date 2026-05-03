from app.domain.vos import Password
from app.domain.models.user import UserModel

import pytest


@pytest.fixture
def user():
    email = "test@example.com"
    password = Password("@aa123456")

    return UserModel(email=email, password=password)


def test_user_creation(user: UserModel):
    assert user.email == "test@example.com"
    assert user.password is not None
    assert user.id is not None


def test_user_login(user: UserModel):
    login_response = user.login()

    assert login_response.access_token is not None
    assert login_response.refresh_token is not None
    assert login_response.created_at is not None
    assert login_response.refresh_expires_at is not None
    assert login_response.jti is not None


def test_refresh_access_token(user: UserModel):
    access_token = user.refresh_access_token()

    assert access_token is not None
