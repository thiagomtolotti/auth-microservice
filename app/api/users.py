from fastapi.routing import APIRouter

from app.services.users import UsersService
from app.utils.types import (
    CreateUserHandlerDTO,
    LoginHandlerDTO,
    LoginHandlerResponseDTO,
    LogoutHandlerDTO,
)


class UsersRouter:
    def __init__(self, service: UsersService):
        self.router = APIRouter(prefix="/users")
        self.service = service

        self.router.add_api_route("/", self.create_user, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])

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
