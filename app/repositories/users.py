from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic.networks import EmailStr

from app.types import CreateUserRepositoryDTO, Password


@dataclass
class UserModel:
    email: EmailStr
    password: Password


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
