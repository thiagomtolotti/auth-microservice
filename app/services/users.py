from uuid import UUID

from pydantic.networks import EmailStr

from app.domain.vos.password import Password

from app.domain.vos.tokens import Token, TokenPayload
from app.utils.types import (
    CreateUserHandlerDTO,
    LoginHandlerDTO,
    LoginServiceResponseDTO,
)
from app.domain.exceptions import (
    LoginFailedException,
    LogoutFailedException,
    UserAlreadyExistsException,
    UserNotFoundException,
)

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
            login_data.refresh_expires_at,
            login_data.jti,
        )

        return LoginServiceResponseDTO(
            access_token=login_data.access_token, refresh_token=login_data.refresh_token
        )

    def logout(self, email: EmailStr):
        user = self.repository.find_by_email(email)

        if not user:
            raise LogoutFailedException("Invalid email address")

        success = self.repository.delete_all_refresh_tokens(user.id)

        if not success:
            raise LogoutFailedException("Failed to log out user")

    def refresh_token(self, refresh_token: str) -> str:
        token = Token.decode(refresh_token)

        user = self.repository.find_by_id(UUID(token.sub))

        if not user:
            raise UserNotFoundException("User not found")

        new_access_token = user.refresh_access_token()

        return new_access_token

    def change_password(self, token: TokenPayload, new_password: str):
        user = self.repository.find_by_id(UUID(token.sub))

        if not user:
            raise UserNotFoundException("User not found")

        user.change_password(new_password)

        self.repository.update_password(user.id, user.password)
