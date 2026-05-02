class DomainException(Exception):
    """Base class for domain exceptions."""

    pass


class InvalidPasswordException(DomainException):
    """Exception raised for invalid passwords."""

    pass


class LoginFailedException(DomainException):
    """Exception raised when login fails."""

    pass


class UserAlreadyExistsException(DomainException):
    """Exception raised when trying to create a user that already exists."""

    pass
