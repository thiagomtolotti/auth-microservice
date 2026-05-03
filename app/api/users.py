from fastapi.routing import APIRouter
from pydantic.main import BaseModel

from app.services.users import UsersService
from app.utils.types import (
    CreateUserHandlerDTO,
    LoginHandlerDTO,
    LoginHandlerResponseDTO,
    LogoutHandlerDTO,
)


class RefreshTokenHandlerDTO(BaseModel):
    refresh_token: str


class RefreshTokenHandlerResponseDTO(BaseModel):
    access_token: str


class UsersRouter:
    def __init__(self, service: UsersService):
        self.router = APIRouter(prefix="/users")
        self.service = service

        self.router.add_api_route("/", self.create_user, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/refresh", self.refresh_token, methods=["POST"])

    def create_user(self, data: CreateUserHandlerDTO):
        self.service.create(data)

        return {"message": "User created successfully"}

    def login(self, data: LoginHandlerDTO) -> LoginHandlerResponseDTO:
        res = self.service.login(data)

        return LoginHandlerResponseDTO(
            access_token=res.access_token,
            refresh_token=res.refresh_token,
        )

    def logout(self, data: LogoutHandlerDTO):
        self.service.logout(data.email)

        return {"message": "User logged out successfully"}

    def refresh_token(
        self, data: RefreshTokenHandlerDTO
    ) -> RefreshTokenHandlerResponseDTO:
        access_token = self.service.refresh_token(data.refresh_token)

        return RefreshTokenHandlerResponseDTO(access_token=access_token)
