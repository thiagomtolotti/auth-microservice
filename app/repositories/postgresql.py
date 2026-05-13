from uuid import UUID

from app.utils.types import CreateUserRepositoryDTO

from .users import User
from .types import ForgotPasswordData, Password, UsersRepository


class PostgreSQLRepository(UsersRepository):
    def __init__(self):
        pass
    
    def create(self, data: CreateUserRepositoryDTO):
        pass

    def find_by_email(self, email: str) -> User | None:
        pass

    def save_refresh_token(
        self, user_id: UUID, created_at: int, expires_at: int, jti: str
    ):
        pass

    def delete_all_refresh_tokens(self, user_id: UUID) -> bool: # type: ignore
        pass

    def find_by_id(self, id: UUID) -> User | None:
        pass

    def update_password(self, user_id: UUID, new_password: Password) -> bool: # type: ignore
        pass

    def is_refresh_token_valid(self, user_id: UUID, jti: str) -> bool: # type: ignore
        pass

    def delete(self, user_id: UUID) -> bool: # type: ignore
        pass
    
    def create_forgot_password_token(self, user_id: UUID, token: str, expires_at: int):
        pass

    def delete_forgot_password_token(self, token: str) -> bool: # type: ignore
        pass

    def find_forgot_password_token(
        self, user_id: UUID, token: str
    ) -> ForgotPasswordData | None:
        pass
