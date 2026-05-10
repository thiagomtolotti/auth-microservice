from typing import Annotated

from fastapi.params import Header

from app.domain.exceptions import InvalidTokenException

from app.domain.vos.tokens import Token, TokenPayload


def _get_auth_token(auth_header: str | None) -> str | None:
    if not auth_header:
        return None

    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]


def require_auth(authorization: Annotated[str | None, Header()] = None) -> TokenPayload:
    token = _get_auth_token(authorization)

    if not token:
        raise InvalidTokenException("Authorization header missing or malformed")

    try:
        return Token.decode(token)
    except Exception:
        raise InvalidTokenException("Invalid token")
