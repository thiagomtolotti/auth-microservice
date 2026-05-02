from app.domain.vos import Password
from app.repositories.users import CreateUserRepositoryDTO, UsersRepository
from app.types import CreateUserHandlerDTO


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def create(self, data: CreateUserHandlerDTO):
        dto = CreateUserRepositoryDTO(
            email=data.email,
            password=Password(data.password),
        )

        self.repository.create(dto)
