from app.domain.exceptions import LoginFailedException, UserAlreadyExistsException
from app.domain.vos import Password
from app.repositories.users import CreateUserRepositoryDTO, UsersRepository
from app.types import CreateUserHandlerDTO, LoginHandlerDTO


class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def create(self, data: CreateUserHandlerDTO):
        exists = bool(self.repository.find_by_email(data.email))

        if exists:
            raise UserAlreadyExistsException("User already exists")

        dto = CreateUserRepositoryDTO(
            email=data.email,
            password=Password(data.password),
        )

        self.repository.create(dto)

    def login(self, data: LoginHandlerDTO):
        user = self.repository.find_by_email(data.email)

        if not user:
            raise LoginFailedException("Invalid email or password")

        if not user.password.verify(data.password):
            raise LoginFailedException("Invalid email or password")
