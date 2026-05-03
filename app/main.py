from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from app.api import DefaultRouter, UsersRouter
from app.domain.exceptions import DomainException
from app.repositories.users import InMemoryUsersRepository
from app.services.users import UsersService
from app.utils import setup_environment


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

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(  # type: ignore
        _: Request, exc: RequestValidationError
    ):
        """
        Transforms the default FastAPI validation error into a
        clean, readable format.
        """
        details: list[dict[str, str]] = []
        for error in exc.errors():
            # error["loc"] usually looks like ("body", "username") or ("query", "limit")
            location = " - ".join([str(loc) for loc in error["loc"]])

            details.append(
                {
                    "field": location,
                    "message": error["msg"].capitalize(),
                    "type": error["type"],
                    "input_provided": error.get(
                        "input"
                    ),  # Shows what the user actually sent
                }
            )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "code": 422,
                "message": "Validation Failed",
                "errors": details,
            },
        )


def initialize():
    print("Initializing the service...")

    setup_environment()

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
