from typing import Annotated

from fastapi.exceptions import HTTPException
from fastapi.params import Header

from app.domain.vos import Token
from app.domain.vos.tokens import TokenPayload


def _get_auth_token(auth_header: str | None) -> str | None:
    if not auth_header:
        return None

    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]


class InvalidTokenException(HTTPException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(status_code=401, detail=detail)


def require_auth(authorization: Annotated[str | None, Header()] = None) -> TokenPayload:
    token = _get_auth_token(authorization)

    if not token:
        raise InvalidTokenException()

    try:
        return Token.decode(token)
    except Exception:
        raise InvalidTokenException()
