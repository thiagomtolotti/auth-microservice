from typing import Any

from fastapi.exceptions import HTTPException, RequestValidationError


class DomainException(Exception):
    """Base class for domain exceptions."""

    pass


class InvalidPasswordException(RequestValidationError):
    def __init__(self, message: str = "Invalid password"):
        # We manually construct the error list to match Pydantic's expected shape
        errors: list[dict[str, Any]] = [
            {
                "loc": ("body", "password"),
                "msg": message,
                "type": "value_error.password_invalid",
            }
        ]
        super().__init__(errors)


class LoginFailedException(DomainException):
    """Exception raised when login fails."""

    pass


class LogoutFailedException(DomainException):
    """Exception raised when logout fails."""

    pass


class UserAlreadyExistsException(DomainException):
    """Exception raised when trying to create a user that already exists."""

    pass


class UserNotFoundException(DomainException):
    """Exception raised when a user is not found."""

    pass


class InvalidTokenException(HTTPException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(status_code=401, detail=detail)
