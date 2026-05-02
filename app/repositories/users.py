from abc import ABC, abstractmethod
from uuid import UUID

from pydantic.networks import EmailStr

from app.domain.models.user import UserModel
from app.types import CreateUserRepositoryDTO


class UsersRepository(ABC):
    @abstractmethod
    def create(self, data: CreateUserRepositoryDTO):
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> UserModel | None:
        pass

    @abstractmethod
    def create_refresh_token(self, user_id: UUID, refresh_token: str):
        pass


class InMemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users: list[UserModel] = []
        self.refresh_tokens: dict[str, str] = {}

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

    def create_refresh_token(self, user_id: UUID, refresh_token: str):
        self.refresh_tokens[str(user_id)] = refresh_token

        print(f"Refresh token created for user_id: {user_id}")
