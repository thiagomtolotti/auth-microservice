from fastapi.routing import APIRouter

from app.services.users import UsersService


class UsersRouter:
    def __init__(self, service: UsersService):
        self.router = APIRouter(prefix="/users")
        self.service = service

        self.router.add_api_route("/", self.create_user, methods=["POST"])

    def create_user(self):
        self.service.create()

        return {"message": "User created successfully"}
