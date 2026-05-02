from fastapi import FastAPI

from app.api import DefaultRouter, UsersRouter
from app.repositories.users import InMemoryUsersRepository
from app.services.users import UsersService


def initialize():
    print("Initializing the service...")

    app = FastAPI()

    users_repo = InMemoryUsersRepository()
    users_service = UsersService(users_repo)

    default_router = DefaultRouter()
    users_router = UsersRouter(users_service)

    app.include_router(default_router.router)
    app.include_router(users_router.router)

    return app


app = initialize()
