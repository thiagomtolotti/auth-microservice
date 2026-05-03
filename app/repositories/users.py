from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from pydantic.networks import EmailStr

from app.domain.models.user import UserModel
from app.utils.types import CreateUserRepositoryDTO
from app.domain.vos import Token


class UsersRepository(ABC):
    @abstractmethod
    def create(self, data: CreateUserRepositoryDTO):
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserModel | None:
        pass

    @abstractmethod
    def save_refresh_token(
        self, user_id: UUID, created_at: int, expires_at: int, jti: str
    ):
        pass

    @abstractmethod
    def delete_all_refresh_tokens(self, user_id: UUID) -> bool:
        """Deletes all refresh tokens for a given user. Returns True if any tokens were deleted, False otherwise."""
        pass

    @abstractmethod
    def find_by_refresh_token(self, refresh_token: str) -> UserModel | None:
        pass


@dataclass
class RefreshTokenData:
    user_id: UUID
    created_at: int
    expires_at: int
    jti: str


class InMemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users: list[UserModel] = []
        self.refresh_tokens: list[RefreshTokenData] = []

    def create(self, data: CreateUserRepositoryDTO):
        user = UserModel(
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

    def find_by_refresh_token(self, refresh_token: str) -> UserModel | None:
        token_data = Token.decode(refresh_token)

        for token in self.refresh_tokens:
            if token.jti == token_data.jti:
                for user in self.users:
                    if user.id == token.user_id:
                        return user

        return None
