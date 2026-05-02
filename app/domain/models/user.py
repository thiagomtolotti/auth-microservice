from pydantic.networks import EmailStr

from app.domain.vos import Password


class UserModel:
    def __init__(self, email: EmailStr, password: Password):
        self.email = email
        self.password = password

    def generate_access_token(self) -> str:
        return f"token-for-{self.email}"
