from fastapi.routing import APIRouter


class Router:
    def __init__(self, router: APIRouter):
        self.router = router

        self.router.add_api_route("/", self.ping, methods=["GET"])

    def ping(self):
        return {"message": "Service is alive"}
