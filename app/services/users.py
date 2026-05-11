import datetime
import random
from uuid import UUID

from app.constants import FORGOT_PASSWORD_TOKEN_DURATION
from app.domain.vos.password import Password

from app.domain.vos.tokens import (
    AccessToken,
    RefreshToken,
)
from app.utils.types import (
    CreateUserHandlerDTO,
    LoginHandlerDTO,
    LoginServiceResponseDTO,
)
from app.domain.exceptions import (
    InvalidPasswordException,
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

        access_token = AccessToken(str(user.id))
        refresh_token = RefreshToken(str(user.id))

        self.repository.save_refresh_token(
            user.id,
            refresh_token.payload.iat,
            refresh_token.payload.exp,
            refresh_token.payload.jti,
        )

        return LoginServiceResponseDTO(
            access_token=str(access_token), refresh_token=str(refresh_token)
        )

    def logout(self, access_token: AccessToken):
        user = self.repository.find_by_id(UUID(access_token.payload.sub))

        if not user:
            raise LogoutFailedException("Invalid email address")

        success = self.repository.delete_all_refresh_tokens(user.id)

        if not success:
            raise LogoutFailedException("Failed to log out user")

    def refresh_token(self, refresh_token: str) -> str:
        token = RefreshToken.decode(refresh_token)

        user = self.repository.find_by_id(UUID(token.payload.sub))

        if not user:
            raise UserNotFoundException("User not found")

        is_valid = self.repository.is_refresh_token_valid(user.id, token.payload.jti)

        if not is_valid:
            raise LoginFailedException("Invalid refresh token")

        new_access_token = AccessToken(sub=str(user.id))

        return str(new_access_token)

    def change_password(self, token: AccessToken, new_password: str):
        user = self.repository.find_by_id(UUID(token.payload.sub))

        if not user:
            raise UserNotFoundException("User not found")

        new_pass = Password(new_password)

        if user.password.verify(new_password):
            raise InvalidPasswordException(
                "New password cannot be the same as the old password"
            )

        self.repository.update_password(user.id, new_pass)

    def delete_user(self, token: AccessToken):
        user = self.repository.find_by_id(UUID(token.payload.sub))

        if not user:
            raise UserNotFoundException("User not found")

        sucess = self.repository.delete(user.id)

        if not sucess:
            raise UserNotFoundException("User not found")

    def find_user(self, user_id: UUID):
        user = self.repository.find_by_id(user_id)

        if not user:
            raise UserNotFoundException("User not found")

        return user

    def forgot_password(self, email: str):
        user = self.repository.find_by_email(email)

        if not user:
            raise UserNotFoundException("User not found")

        token = ForgotPasswordToken()

        self.repository.create_forgot_password_token(
            user.id, str(token), expires_at=token.expires_at
        )

        print(f"Forgot password token for user {email}: {token.token}")


class ForgotPasswordToken:
    def __init__(self):
        self.token = random.randint(1000, 9999)

        now = datetime.datetime.now(datetime.timezone.utc)
        expires_delta = datetime.timedelta(seconds=FORGOT_PASSWORD_TOKEN_DURATION)

        self.expires_at = int((now + expires_delta).timestamp())
