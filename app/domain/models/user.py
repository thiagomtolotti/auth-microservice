from dataclasses import dataclass
from uuid import uuid4
import datetime

from pydantic.networks import EmailStr

from app.domain.vos import Password, AccessToken, RefreshToken, CreateTokenPayload


@dataclass
class LoginResponseData:
    access_token: str
    refresh_token: str
    created_at: int
    refresh_expires_at: int
    jti: str


class UserModel:
    def __init__(self, email: EmailStr, password: Password):
        self.id = uuid4()
        self.email = email
        self.password = password

    def login(self) -> LoginResponseData:
        now = datetime.datetime.now(datetime.timezone.utc)
        session_duration = datetime.timedelta(days=7)

        refresh_expires = now + session_duration

        access_token = AccessToken(
            CreateTokenPayload(
                sub=str(self.id), duration=datetime.timedelta(minutes=0.25)
            )
        ).get()
        refresh_token = RefreshToken(
            CreateTokenPayload(sub=str(self.id), duration=session_duration)
        )
        refresh_token_str = refresh_token.get()

        return LoginResponseData(
            access_token=access_token,
            refresh_token=refresh_token_str,
            created_at=int(now.timestamp()),
            refresh_expires_at=int(refresh_expires.timestamp()),
            jti=str(refresh_token.jti),
        )

    def refresh_access_token(self) -> str:
        access_token = AccessToken(
            CreateTokenPayload(
                sub=str(self.id), duration=datetime.timedelta(minutes=0.5)
            )
        ).get()

        return access_token
