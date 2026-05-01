from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.main import Router


def initialize():
    print("Initializing the service...")

    app = FastAPI()
    router = APIRouter()

    Router(router)

    app.include_router(router)

    return app


app = initialize()
