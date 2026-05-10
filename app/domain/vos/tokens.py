import jwt
import datetime
from abc import ABC
from uuid import uuid4
from dataclasses import dataclass

from app.utils import settings
from app.constants import ACCESS_TOKEN_DURATION, REFRESH_TOKEN_DURATION


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

    def __str__(self) -> str:
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
    def __init__(self, sub: str):
        payload = CreateTokenPayload(
            sub=sub, duration=datetime.timedelta(seconds=ACCESS_TOKEN_DURATION)
        )
        super().__init__(payload, token_type="access")


class RefreshToken(Token):
    def __init__(self, sub: str):
        payload = CreateTokenPayload(
            sub=sub, duration=datetime.timedelta(seconds=REFRESH_TOKEN_DURATION)
        )
        super().__init__(payload, token_type="refresh")
