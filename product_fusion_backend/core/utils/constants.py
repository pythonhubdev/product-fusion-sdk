from typing import Type, TypedDict

from pydantic import BaseModel

from product_fusion_backend.core.schema.common_response_schema import CommonResponseSchema


class RouteOptions(TypedDict):
    response_model_exclude_none: bool
    response_model: Type[BaseModel]


DEFAULT_ROUTE_OPTIONS: RouteOptions = {
    "response_model_exclude_none": True,
    "response_model": CommonResponseSchema,
}

EMAIL_TEMPLATE = """<html> <body> <p>Hello,</p> <p>You have requested to reset your password. Please click the link
below to reset your password:</p> <a>{}</a> <p>This link will expire in 1 hour.</p> <p>If you
did not request this, please ignore this email.</p> </body> </html>"""

SKIP_URLS = [
    "/api/health",
    "/api/openapi.json",
    "/api/docs",
    "/api/redoc",
    "/api/auth",
    "/api/auth/login",
]
