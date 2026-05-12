from argon2 import PasswordHasher
import re

from ..exceptions import InvalidPasswordException


PASSWORD_REGEX = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()_+[\]{};\':"\\|,.<>/?]).+$'

ph = PasswordHasher()


class Password:
    def __init__(self, password: str):

        self.value = password
        self._validate()
        self.hashed = self._hash()

    def _validate(self):
        if not self.value:
            raise InvalidPasswordException("Password cannot be empty")

        if len(self.value) < 8:
            raise InvalidPasswordException(
                "Password must be at least 8 characters long"
            )

        if not re.match(PASSWORD_REGEX, self.value):
            raise InvalidPasswordException(
                "Password must contain at least one letter, one number, and one special character"
            )

    def _hash(self):
        return ph.hash(self.value)

    def verify(self, password: str) -> bool:
        try:
            return ph.verify(self.hashed, password)
        except Exception:
            return False
