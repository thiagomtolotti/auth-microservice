from uuid import UUID
from dataclasses import dataclass
from abc import ABC, abstractmethod

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


@dataclass
class ForgotPasswordData:
    user_id: UUID
    token: str
    expires_at: int

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

    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        """Deletes a user by their ID. Returns True if the user was deleted successfully, False otherwise."""
        pass

    @abstractmethod
    def create_forgot_password_token(self, user_id: UUID, token: str, expires_at: int):
        """Creates a forgot password token for a given user."""
        pass

    @abstractmethod
    def find_forgot_password_token(
        self, user_id: UUID, token: str
    ) -> ForgotPasswordData | None:
        """Finds a forgot password token. Returns the token data if found, None otherwise."""
        pass

    @abstractmethod
    def delete_forgot_password_token(self, token: str) -> bool:
        """Deletes a forgot password token. Returns True if the token was deleted successfully, False otherwise."""
        pass

