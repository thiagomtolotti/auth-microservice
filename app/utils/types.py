from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr

from app.domain.vos.password import Password


class CreateUserHandlerDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


@dataclass
class CreateUserRepositoryDTO:
    email: EmailStr
    password: Password


class LoginHandlerDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


@dataclass
class LoginServiceResponseDTO:
    access_token: str
    refresh_token: str


class LoginHandlerResponseDTO(BaseModel):
    message: str = "Login successful"
    access_token: str
    refresh_token: str


@dataclass
class ChangePasswordHandlerDTO:
    new_password: str


@dataclass
class ForgotPasswordHandlerDTO:
    email: EmailStr


class AuthNotificationHandler(ABC):
    @abstractmethod
    def on_forgot_password(self, email: str, token: str, expires_at: int):
        pass
