from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from .api import DefaultRouter
from .domain.exceptions import DomainException


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
        print(
            f"Validation error: {exc.errors()}"
        )  # Log the validation errors for debugging

        error = exc.errors()[0]

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "type": "ValidationError",
                "detail": f"{error['msg']}",
            },
        )


def initialize():
    print("Initializing the service...")

    app = FastAPI()

    app.include_router(DefaultRouter())

    setup_exception_handlers(app)

    return app


app = initialize()
