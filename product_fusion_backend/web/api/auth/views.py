from fastapi import APIRouter, Depends, Query, Request
from fastapi.security import OAuth2PasswordBearer

from product_fusion_backend.core import APIResponse
from product_fusion_backend.web.api.auth.controller import AuthController
from product_fusion_backend.web.api.auth.schema import LoginSchema, ResetPasswordSchema, SignupSchema

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("")
async def signup(request: SignupSchema) -> APIResponse:
    return await AuthController.signup(request)


@auth_router.post("/login")
async def login(request: LoginSchema) -> APIResponse:
    return await AuthController.login(request)


@auth_router.post("/refresh")
async def refresh_token(token: str = Depends(oauth2_scheme)) -> APIResponse:
    return await AuthController.refresh_token(token)


@auth_router.post("/request-reset-password")
async def request_reset_password(request: Request) -> APIResponse:
    user_id = request.state.user_id
    return await AuthController.request_password_reset(user_id)


@auth_router.post("/reset-password")
async def reset_password(
    reset_data: ResetPasswordSchema,
    token: str = Query(..., description="Reset token from email"),
) -> APIResponse:
    return await AuthController.reset_password(token, reset_data.password)
