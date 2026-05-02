from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.api import DefaultRouter, UsersRouter
from app.domain.exceptions import DomainException
from app.repositories.users import InMemoryUsersRepository
from app.services.users import UsersService


def setup_exception_handlers(app: FastAPI):
    """
    Registers all exception handlers for the application.
    This keeps the 'initialize' function focused on wiring.
    """

    @app.exception_handler(DomainException)
    def domain_exception_handler(_: Request, exc: DomainException):  # type: ignore
        return JSONResponse(
            status_code=400,
            content={"type": exc.__class__.__name__, "detail": str(exc)},
        )


def initialize():
    print("Initializing the service...")

    app = FastAPI()

    users_repo = InMemoryUsersRepository()
    users_service = UsersService(users_repo)

    default_router = DefaultRouter()
    users_router = UsersRouter(users_service)

    app.include_router(default_router.router)
    app.include_router(users_router.router)

    setup_exception_handlers(app)

    return app


app = initialize()
