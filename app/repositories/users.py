from abc import ABC, abstractmethod

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


class InMemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users: list[UserModel] = []

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
