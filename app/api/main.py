from fastapi import Depends
from fastapi.routing import APIRouter

from pydantic.main import BaseModel
from ..dependencies import get_users_service
from ..domain.vos.tokens import AccessToken
from ..routes import Routes
from ..services.users import UsersService
from ..utils.types import (
    CreateUserHandlerDTO,
    LoginHandlerDTO,
    LoginHandlerResponseDTO,
    ChangePasswordHandlerDTO,
    ForgotPasswordHandlerDTO,
    ResetPasswordHandlerDTO,
)
from .require_auth import require_auth


class RefreshTokenHandlerDTO(BaseModel):
    refresh_token: str


class RefreshTokenHandlerResponseDTO(BaseModel):
    access_token: str


class DefaultRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/auth")

        # fmt: off
        self.router.add_api_route(
            Routes.PING.value, self.ping, methods=["GET"]
        )
        # fmt: off
        self.router.add_api_route(
            Routes.PROTECTED.value, self.protected_route, methods=["GET"]
        )
        self.router.add_api_route(
            Routes.REGISTER.value, self.create_user, methods=["POST"]
        )
        # fmt: off
        self.router.add_api_route(
            Routes.LOGIN.value, self.login, methods=["POST"]
        )
        # fmt: off
        self.router.add_api_route(
            Routes.LOGOUT.value, self.logout, methods=["POST"]
        )
        self.router.add_api_route(
            Routes.REFRESH_TOKEN.value, self.refresh_token, methods=["POST"]
        )
        self.router.add_api_route(
            Routes.CHANGE_PASSWORD.value, self.change_password, methods=["POST"]
        )
        self.router.add_api_route(
            Routes.DELETE_USER.value, self.delete_user, methods=["DELETE"]
        )
        self.router.add_api_route(
            Routes.FORGOT_PASSWORD.value, self.forgot_password, methods=["POST"]
        )
        self.router.add_api_route(
            Routes.RESET_PASSWORD.value, self.reset_password, methods=["POST"]
        )

    def ping(self):
        return {"message": "Service is alive"}

    def protected_route(self, _=Depends(require_auth)):
        return {"message": "This is a protected route!"}

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

    def forgot_password(
        self,
        data: ForgotPasswordHandlerDTO,
        service: UsersService = Depends(get_users_service),
    ):
        try:
            service.forgot_password(data.email)

        except Exception as e:
            print(f"Error occurred while processing forgot password request: {e}")
        finally:
            return {
                "message": "If an account with that email exists, a forgot password token has been sent"
            }

    def reset_password(
        self,
        data: ResetPasswordHandlerDTO,
        service: UsersService = Depends(get_users_service),
    ):
        service.reset_password(data.email, data.token, data.new_password)

        return {"message": "Password reset successfully"}
