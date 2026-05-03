from dataclasses import dataclass

from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr

from app.domain.vos import Password


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


class LogoutHandlerDTO(BaseModel):
    email: EmailStr
