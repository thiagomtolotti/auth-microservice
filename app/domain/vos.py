import re

from app.domain.exceptions import InvalidPasswordException


PASSWORD_REGEX = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};\':"\\|,.<>/?]).+$'


class Password:
    def __init__(self, password: str):
        if not password:
            raise InvalidPasswordException("Password cannot be empty")

        if len(password) < 8:
            raise InvalidPasswordException(
                "Password must be at least 8 characters long"
            )

        if not re.match(PASSWORD_REGEX, password):
            raise InvalidPasswordException(
                "Password must contain at least one letter, one number, and one special character"
            )

        self.value = password
