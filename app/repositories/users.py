from abc import ABC, abstractmethod


class UsersRepository(ABC):
    @abstractmethod
    def create(self):
        pass


class InMemoryUsersRepository(UsersRepository):
    def create(self):
        print("Inserting user in repository")
