from authlib.jose import JoseError, jwt
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from product_fusion_backend.core import SKIP_URLS, APIResponse, StatusEnum
from product_fusion_backend.settings import settings


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in SKIP_URLS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return APIResponse(
                status_code=401,
                message="Authorization header is required",
                status_=StatusEnum.ERROR,
            )

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return APIResponse(
                    status_code=401,
                    message="Invalid token type",
                    status_=StatusEnum.ERROR,
                )
            payload = jwt.decode(token, settings.secret_key)
            request.state.user_id = payload.get("sub")
        except (ValueError, JoseError):
            return APIResponse(
                status_code=401,
                message="Invalid token",
                status_=StatusEnum.ERROR,
            )

        return await call_next(request)
