import datetime

from uuid import UUID, uuid4

from pydantic.networks import EmailStr

from ..domain.vos.password import Password
from ..utils.types import CreateUserRepositoryDTO

from .types import ForgotPasswordData, RefreshTokenData, User, UsersRepository


class InMemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users: list[User] = []
        self.refresh_tokens: list[RefreshTokenData] = []
        self.forgot_password_tokens: list[ForgotPasswordData] = []

    def create(self, data: CreateUserRepositoryDTO):
        user = User(
            id=uuid4(),
            email=data.email,
            password=data.password,
        )

        self.users.append(user)

        print(f"User created: {user.email}, id: {user.id}")

    def find_by_email(self, email: EmailStr):
        for user in self.users:
            if user.email == email:
                return user

        return None

    def save_refresh_token(
        self, user_id: UUID, created_at: int, expires_at: int, jti: str
    ):
        self.refresh_tokens.append(
            RefreshTokenData(
                user_id=user_id,
                created_at=created_at,
                expires_at=expires_at,
                jti=jti,
            )
        )

        print(f"Refresh token created for user_id: {user_id}")
        print(f"Current refresh tokens: {len(self.refresh_tokens)}")

    def delete_all_refresh_tokens(self, user_id: UUID) -> bool:
        prev_count = len(self.refresh_tokens)

        self.refresh_tokens = [
            token for token in self.refresh_tokens if token.user_id != user_id
        ]

        after_count = len(self.refresh_tokens)

        print(f"Current refresh tokens: {len(self.refresh_tokens)}")
        return prev_count > after_count

    def is_refresh_token_valid(self, user_id: UUID, jti: str) -> bool:
        now = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

        for token in self.refresh_tokens:
            if token.user_id == user_id and token.jti == jti and token.expires_at > now:
                return True

        return False

    def find_by_id(self, id: UUID) -> User | None:
        for user in self.users:
            if user.id == id:
                return user

        return None

    def update_password(self, user_id: UUID, new_password: Password) -> bool:
        for user in self.users:
            if user.id == user_id:
                user.password = new_password
                return True

        return False

    def delete(self, user_id: UUID) -> bool:
        prev_count = len(self.users)

        self.users = [user for user in self.users if user.id != user_id]

        after_count = len(self.users)

        return prev_count > after_count

    def create_forgot_password_token(self, user_id: UUID, token: str, expires_at: int):
        self.forgot_password_tokens.append(
            ForgotPasswordData(
                user_id=user_id,
                token=token,
                expires_at=expires_at,
            )
        )

        print(f"Forgot password token created for user_id: {user_id}")
        print(f"Current forgot password tokens: {len(self.forgot_password_tokens)}")

    def find_forgot_password_token(
        self, user_id: UUID, token: str
    ) -> ForgotPasswordData | None:
        for t in self.forgot_password_tokens:
            if t.token == token and t.user_id == user_id:
                return t

        return None

    def delete_forgot_password_token(self, token: str) -> bool:
        prev_count = len(self.forgot_password_tokens)

        self.forgot_password_tokens = [
            t for t in self.forgot_password_tokens if t.token != token
        ]

        after_count = len(self.forgot_password_tokens)

        return prev_count > after_count
