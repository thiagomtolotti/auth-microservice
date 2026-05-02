from app.repositories.users import UsersRepository
from app.types import CreateUserHandlerDTO


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def create(self, data: CreateUserHandlerDTO):
        print("Creating User")
        self.repository.create()
