from fastapi.routing import APIRouter

from app.services.users import UsersService
from app.types import CreateUserHandlerDTO


class UsersRouter:
    def __init__(self, service: UsersService):
        self.router = APIRouter(prefix="/users")
        self.service = service

        self.router.add_api_route("/", self.create_user, methods=["POST"])

    def create_user(self, data: CreateUserHandlerDTO):
        self.service.create(data)

        return {"message": "User created successfully"}
