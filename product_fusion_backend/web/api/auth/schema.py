from typing import Any

from pydantic import BaseModel, EmailStr


class BaseAuthSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(BaseAuthSchema):
    pass


class SignupSchema(BaseAuthSchema):
    organization_name: str
    organization_status: int = 0
    organization_personal: bool = False
    organization_settings: dict[str, Any] = {}


class ResetPasswordSchema(BaseModel):
    password: str
