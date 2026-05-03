from app.domain.vos import Password

from app.utils.types import (
    CreateUserHandlerDTO,
    LoginHandlerDTO,
    LoginServiceResponseDTO,
)
from app.domain.exceptions import LoginFailedException, UserAlreadyExistsException

from app.repositories.users import CreateUserRepositoryDTO, UsersRepository


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

    def login(self, data: LoginHandlerDTO) -> LoginServiceResponseDTO:
        user = self.repository.find_by_email(data.email)

        if not user:
            raise LoginFailedException("Invalid email or password")

        if not user.password.verify(data.password):
            raise LoginFailedException("Invalid email or password")

        login_data = user.login()

        self.repository.save_refresh_token(
            user.id,
            login_data.created_at,
            login_data.expires_at,
            login_data.jti,
        )

        return LoginServiceResponseDTO(
            access_token=login_data.access_token, refresh_token=login_data.refresh_token
        )
