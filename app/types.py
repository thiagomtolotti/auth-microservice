from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import EmailStr


class CreateUserHandlerDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
