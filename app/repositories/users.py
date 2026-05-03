from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from pydantic.networks import EmailStr

from app.domain.models.user import UserModel
from app.utils.types import CreateUserRepositoryDTO


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


@dataclass
class RefreshTokenData:
    user_id: UUID
    created_at: int
    expires_at: int
    jti: str


class InMemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users: list[UserModel] = []
        self.refresh_tokens: dict[str, RefreshTokenData] = {}

    def create(self, data: CreateUserRepositoryDTO):
        user = UserModel(
            email=data.email,
            password=data.password,
        )

        self.users.append(user)

        print(f"User created: {user.email}")

    def find_by_email(self, email: EmailStr):
        for user in self.users:
            if user.email == email:
                return user

        return None

    def save_refresh_token(
        self, user_id: UUID, created_at: int, expires_at: int, jti: str
    ):
        self.refresh_tokens[str(user_id)] = RefreshTokenData(
            user_id=user_id,
            created_at=created_at,
            expires_at=expires_at,
            jti=jti,
        )

        print(f"Refresh token created for user_id: {user_id}")
