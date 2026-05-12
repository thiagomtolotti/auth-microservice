import jwt
import datetime
from abc import ABC
from uuid import UUID, uuid4
from dataclasses import dataclass

from ...utils import settings
from ...constants import ACCESS_TOKEN_DURATION, REFRESH_TOKEN_DURATION

from ..exceptions import InvalidTokenException


@dataclass
class CreateTokenPayload:
    sub: str
    duration: datetime.timedelta


@dataclass
class TokenPayload:
    sub: str
    iat: int
    exp: int
    type: str
    jti: str


class Token(ABC):
    def __init__(
        self, payload: CreateTokenPayload, token_type: str, jti: UUID = uuid4()
    ):
        self.jti = jti

        now = datetime.datetime.now(datetime.timezone.utc)
        exp = now + payload.duration

        self.payload: TokenPayload = TokenPayload(
            sub=payload.sub,
            iat=int(now.timestamp()),
            exp=int(exp.timestamp()),
            type=token_type,
            jti=str(jti),
        )

    def __str__(self) -> str:
        return str(
            jwt.encode(
                self.payload.__dict__, settings.private_key.encode(), algorithm="RS256"
            )
        )

    @staticmethod
    def _decode(token: str) -> TokenPayload:
        try:
            decoded = jwt.decode(
                token, settings.public_key.encode(), algorithms=["RS256"]
            )
        except jwt.PyJWTError:
            raise InvalidTokenException("Invalid token")

        return TokenPayload(**decoded)


class AccessToken(Token):
    def __init__(self, sub: str, jti: UUID = uuid4()):
        payload = CreateTokenPayload(
            sub=sub, duration=datetime.timedelta(seconds=ACCESS_TOKEN_DURATION)
        )
        super().__init__(payload, token_type="access", jti=jti)

    @staticmethod
    def decode(token: str) -> "AccessToken":
        payload = Token._decode(token)

        if payload.type != "access":
            raise InvalidTokenException("Invalid token type")

        return AccessToken(sub=payload.sub, jti=UUID(payload.jti))


class RefreshToken(Token):
    def __init__(self, sub: str, jti: UUID = uuid4()):
        payload = CreateTokenPayload(
            sub=sub, duration=datetime.timedelta(seconds=REFRESH_TOKEN_DURATION)
        )
        super().__init__(payload, token_type="refresh", jti=jti)

    @staticmethod
    def decode(token: str) -> "RefreshToken":
        payload = Token._decode(token)

        if payload.type != "refresh":
            raise InvalidTokenException("Invalid token type")

        return RefreshToken(sub=payload.sub, jti=UUID(payload.jti))
