from authlib.jose import JoseError, jwt
from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from product_fusion_backend.settings import settings


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in ["/api/auth/signup", "/api/auth/login"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
            payload = jwt.decode(token, settings.secret_key)
            request.state.user_id = payload.get("sub")
        except (ValueError, JoseError):
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return await call_next(request)
