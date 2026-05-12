import pytest

from .domain.vos.password import Password


def test_valid_password():
    password = Password("@aa123456")

    assert password is not None


def test_invalid_password_empty():
    with pytest.raises(Exception) as exc_info:
        Password("")
    assert exc_info.value.args[0] == "Password cannot be empty"


def test_invalid_password_short():
    with pytest.raises(Exception) as exc_info:
        Password("@aa123")
    assert exc_info.value.args[0] == "Password must be at least 8 characters long"


def test_invalid_password_no_letter():
    with pytest.raises(Exception) as exc_info:
        Password("@12345678")
    assert (
        exc_info.value.args[0]
        == "Password must contain at least one letter, one number, and one special character"
    )


def test_invalid_password_no_number():
    with pytest.raises(Exception) as exc_info:
        Password("@abcdefgh")
    assert (
        exc_info.value.args[0]
        == "Password must contain at least one letter, one number, and one special character"
    )


def test_invalid_password_no_special_char():
    with pytest.raises(Exception) as exc_info:
        Password("aa12345678")
    assert (
        exc_info.value.args[0]
        == "Password must contain at least one letter, one number, and one special character"
    )


def test_password_verification():
    password = Password("@aa123456")

    assert password.verify("@aa123456") is True
    assert password.verify("wrongpassword") is False


def test_password_hashing():
    password = Password("@aa123456")

    assert password.hashed != password.value


def test_password_hashing_consistency():
    password = Password("@aa123456")

    hashed1 = password.hashed
    hashed2 = password._hash()  # type: ignore

    assert hashed1 != hashed2
