import datetime

from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID, uuid4

from pydantic.networks import EmailStr

from app.domain.vos.password import Password
from app.utils.types import CreateUserRepositoryDTO


@dataclass
class RefreshTokenData:
    user_id: UUID
    created_at: int
    expires_at: int
    jti: str


@dataclass
class User:
    email: EmailStr
    password: Password
    id: UUID


class UsersRepository(ABC):
    @abstractmethod
    def create(self, data: CreateUserRepositoryDTO):
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
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
    def find_by_id(self, id: UUID) -> User | None:
        pass

    @abstractmethod
    def update_password(self, user_id: UUID, new_password: Password) -> bool:
        """Updates the password for a given user. Returns True if the password was updated successfully, False otherwise."""

        pass

    @abstractmethod
    def is_refresh_token_valid(self, user_id: UUID, jti: str) -> bool:
        """Checks if a refresh token is valid for a given user. Returns True if the token is valid, False otherwise."""
        pass


class InMemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users: list[User] = []
        self.refresh_tokens: list[RefreshTokenData] = []

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
