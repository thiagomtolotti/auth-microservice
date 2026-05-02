from abc import ABC, abstractmethod

from pydantic.main import BaseModel

from app.types import CreateUserRepositoryDTO


class UsersRepository(ABC):
    @abstractmethod
    def create(self, data: CreateUserRepositoryDTO):
        pass


class InMemoryUser(BaseModel):
    email: str
    password: str


class InMemoryUsersRepository(UsersRepository):
    def __init__(self):
        self.users: list[InMemoryUser] = []

    def create(self, data: CreateUserRepositoryDTO):
        user = InMemoryUser(email=data.email, password=data.password.value)

        self.users.append(user)

        print(f"User created: {user.email}")
