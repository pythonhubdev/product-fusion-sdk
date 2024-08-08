from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from product_fusion_backend.core import APIResponse
from product_fusion_backend.web.api.auth.schema import LoginSchema, SignupSchema
from product_fusion_backend.web.api.auth.service import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("/signup")
async def signup(request: SignupSchema) -> APIResponse:
    return await AuthService.signup(request)


@auth_router.post("/login")
async def login(request: LoginSchema) -> APIResponse:
    return await AuthService.login(request)


@auth_router.post("/refresh")
async def refresh_token(token: str = Depends(oauth2_scheme)) -> APIResponse:
    return await AuthService.refresh_token(token)
