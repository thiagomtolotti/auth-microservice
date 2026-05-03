from fastapi.params import Header
from fastapi.routing import APIRouter
from starlette.responses import JSONResponse
from typing_extensions import Annotated

from app.domain.vos import Token


class DefaultRouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route("/", self.ping, methods=["GET"])
        self.router.add_api_route("/protected", self.protected_route, methods=["GET"])

    def ping(self):
        return {"message": "Service is alive"}

    def protected_route(self, authorization: Annotated[str | None, Header()] = None):
        token = authorization.split(" ")[1] if authorization else None

        if not token:
            return JSONResponse(
                status_code=401, content={"message": "Authorization header missing"}
            )

        try:
            Token.decode(token)
        except Exception:
            return JSONResponse(status_code=401, content={"message": "Invalid token"})

        return {"message": "This is a protected route"}
