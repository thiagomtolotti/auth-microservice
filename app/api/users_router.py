from fastapi import Depends
from fastapi.routing import APIRouter

from pydantic.main import BaseModel
from app.dependencies import get_users_service
from app.domain.vos.tokens import AccessToken
from app.services.users import UsersService
from app.utils.types import (
    CreateUserHandlerDTO,
    LoginHandlerDTO,
    LoginHandlerResponseDTO,
    ChangePasswordHandlerDTO,
)
from .require_auth import require_auth


class RefreshTokenHandlerDTO(BaseModel):
    refresh_token: str


class RefreshTokenHandlerResponseDTO(BaseModel):
    access_token: str


class UsersRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/users")

        self.router.add_api_route("/", self.create_user, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])
        self.router.add_api_route("/refresh", self.refresh_token, methods=["POST"])
        self.router.add_api_route(
            "/change_password", self.change_password, methods=["POST"]
        )
        self.router.add_api_route("/", self.delete_user, methods=["DELETE"])

    def create_user(
        self,
        data: CreateUserHandlerDTO,
        service: UsersService = Depends(get_users_service),
    ):
        service.create(data)

        return {"message": "User created successfully"}

    def login(
        self, data: LoginHandlerDTO, service: UsersService = Depends(get_users_service)
    ) -> LoginHandlerResponseDTO:
        res = service.login(data)

        return LoginHandlerResponseDTO(
            access_token=res.access_token,
            refresh_token=res.refresh_token,
        )

    def logout(
        self,
        service: UsersService = Depends(get_users_service),
        access_token: AccessToken = Depends(require_auth),
    ):
        service.logout(access_token)

        return {"message": "Successfully logged out"}

    def refresh_token(
        self,
        data: RefreshTokenHandlerDTO,
        service: UsersService = Depends(get_users_service),
    ) -> RefreshTokenHandlerResponseDTO:
        access_token = service.refresh_token(data.refresh_token)

        return RefreshTokenHandlerResponseDTO(access_token=access_token)

    def change_password(
        self,
        data: ChangePasswordHandlerDTO,
        access_token: AccessToken = Depends(require_auth),
        service: UsersService = Depends(get_users_service),
    ):
        service.change_password(access_token, new_password=data.new_password)

        return {"message": "Password changed successfully"}

    def delete_user(
        self,
        access_token: AccessToken = Depends(require_auth),
        service: UsersService = Depends(get_users_service),
    ):
        service.delete_user(access_token)

        return {"message": "User deleted successfully"}
