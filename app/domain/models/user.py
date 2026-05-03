from dataclasses import dataclass
import datetime
from uuid import UUID, uuid4
import jwt

from pydantic.networks import EmailStr

from app.utils import private_key
from app.domain.vos import Password


@dataclass
class LoginResponseData:
    access_token: str
    refresh_token: str
    created_at: int
    expires_at: int
    jti: str


class UserModel:
    def __init__(self, email: EmailStr, password: Password):
        self.id = uuid4()
        self.email = email
        self.password = password

    def login(self) -> LoginResponseData:
        jti = uuid4()

        now = datetime.datetime.now(datetime.timezone.utc)
        session_duration = datetime.timedelta(days=7)

        refresh_expires = now + session_duration

        access_token = self._generate_access_token()
        refresh_token = self._generate_refresh_token(jti, now, refresh_expires)

        return LoginResponseData(
            access_token=access_token,
            refresh_token=refresh_token,
            created_at=int(now.timestamp()),
            expires_at=int(refresh_expires.timestamp()),
            jti=str(jti),
        )

    def _generate_access_token(self) -> str:
        now = datetime.datetime.now()
        duration = datetime.timedelta(minutes=15)

        expiration_date = now + duration

        payload: dict[str, str | datetime.datetime] = {
            "sub": str(self.id),
            "exp": expiration_date,
            "iat": now,  # Issued At Time
            "type": "access",
        }

        return str(jwt.encode(payload, private_key, algorithm="HS256"))

    def _generate_refresh_token(
        self, jti: UUID, now: datetime.datetime, exp: datetime.datetime
    ) -> str:
        payload: dict[str, str | datetime.datetime] = {
            "sub": str(self.id),
            "exp": exp,
            "iat": now,  # Issued At Time
            "jti": str(jti),  # Unique identifier for the token
            "type": "refresh",
        }

        return str(jwt.encode(payload, private_key, algorithm="HS256"))
