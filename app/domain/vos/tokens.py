from abc import ABC
from dataclasses import dataclass
from uuid import uuid4
import datetime
import jwt

from app.utils import settings


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
    def __init__(self, payload: CreateTokenPayload, token_type: str):
        jti = uuid4()

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

    def get(self) -> str:
        return str(
            jwt.encode(
                self.payload.__dict__, settings.private_key.encode(), algorithm="RS256"
            )
        )

    @staticmethod
    def decode(token: str) -> TokenPayload:
        decoded = jwt.decode(token, settings.public_key.encode(), algorithms=["RS256"])

        return TokenPayload(**decoded)


class AccessToken(Token):
    def __init__(self, payload: CreateTokenPayload):
        super().__init__(payload, token_type="access")


class RefreshToken(Token):
    def __init__(self, payload: CreateTokenPayload):
        super().__init__(payload, token_type="refresh")
