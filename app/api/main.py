from fastapi.routing import APIRouter


class DefaultRouter:
    def __init__(self):
        self.router = APIRouter()

        self.router.add_api_route("/", self.ping, methods=["GET"])

    def ping(self):
        return {"message": "Service is alive"}
