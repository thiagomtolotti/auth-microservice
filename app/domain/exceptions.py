class DomainException(Exception):
    """Base class for domain exceptions."""

    pass


class InvalidPasswordException(DomainException):
    """Exception raised for invalid passwords."""

    pass


class LoginFailedException(DomainException):
    """Exception raised when login fails."""

    pass
