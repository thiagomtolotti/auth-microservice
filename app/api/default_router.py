from fastapi import Depends
from fastapi.routing import APIRouter

from .require_auth import require_auth


class DefaultRouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route("/", self.ping, methods=["GET"])
        self.router.add_api_route("/protected", self.protected_route, methods=["GET"])

    def ping(self):
        return {"message": "Service is alive"}

    def protected_route(self, _=Depends(require_auth)):
        return {"message": "This is a protected route"}
