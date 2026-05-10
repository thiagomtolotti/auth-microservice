from typing import Annotated
from uuid import UUID

from fastapi.params import Header
from fastapi import Depends

from app.dependencies import get_users_service
from app.domain.exceptions import InvalidTokenException
from app.domain.vos.tokens import AccessToken
from app.services.users import UsersService


def _get_auth_token(auth_header: str | None) -> str | None:
    if not auth_header:
        return None

    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]


def require_auth(
    authorization: Annotated[str | None, Header()] = None,
    service: UsersService = Depends(get_users_service),
) -> AccessToken:
    token = _get_auth_token(authorization)

    if not token:
        raise InvalidTokenException("Authorization header missing or malformed")

    token = AccessToken.decode(token)

    user = service.find_user(UUID(token.payload.sub))

    if not user:
        raise InvalidTokenException("User not found")

    return token
