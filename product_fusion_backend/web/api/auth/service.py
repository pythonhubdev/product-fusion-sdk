from datetime import UTC, datetime, timedelta

from authlib.jose import jwt
from starlette import status

from product_fusion_backend.core import APIResponse, StatusEnum
from product_fusion_backend.core.utils.hash_utils import hash_manager
from product_fusion_backend.dao import MemberDAO, OrganizationDAO, RoleDAO, UserDAO
from product_fusion_backend.settings import settings
from product_fusion_backend.web.api.auth.schema import LoginSchema, SignupSchema

member_dao = MemberDAO()
user_dao = UserDAO()
org_dao = OrganizationDAO()
role_dao = RoleDAO()


class AuthService:
    @staticmethod
    async def signup(request: SignupSchema) -> APIResponse:
        try:
            existing_user = await user_dao.get_by_email(request.email)  # type: ignore
            if existing_user:
                return APIResponse(
                    status_=StatusEnum.ERROR,
                    message="Email already registered",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            hashed_password = hash_manager.hash_password(request.password)
            user_data = {
                "email": request.email,
                "password": hashed_password,
            }
            new_user = await user_dao.create(user_data)  # type: ignore

            org = await org_dao.get_by_name(request.organization_name)  # type: ignore
            if not org:
                org = await org_dao.create(  # type: ignore
                    {
                        "name": request.organization_name,
                        "status": request.organization_status,
                        "personal": request.organization_personal,
                        "settings": request.organization_settings,
                    },
                )

            owner_role = await role_dao.get_by_name_and_org("owner", org.id)  # type: ignore
            if not owner_role:
                owner_role = await role_dao.create(  # type: ignore
                    {
                        "name": "owner",
                        "org_id": org.id,
                    },
                )

            await member_dao.create(  # type: ignore
                {
                    "user_id": new_user.id,
                    "org_id": org.id,
                    "role_id": owner_role.id,
                },
            )

            access_token = AuthService.create_access_token(new_user.id)
            refresh_token = AuthService.create_refresh_token(new_user.id)
            return APIResponse(
                status_=StatusEnum.SUCCESS,
                message="User registered successfully",
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                },
                status_code=status.HTTP_201_CREATED,
            )
        except Exception as exception:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message=f"An error occurred: {str(exception)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    async def login(request: LoginSchema) -> APIResponse:
        try:
            user = await user_dao.get_by_email(request.email)  # type: ignore
            if not user or not hash_manager.verify_password(request.password, user.password):
                return APIResponse(
                    status_=StatusEnum.ERROR,
                    message="Incorrect email or password",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            access_token = AuthService.create_access_token(user.id)
            refresh_token = AuthService.create_refresh_token(user.id)
            return APIResponse(
                status_=StatusEnum.SUCCESS,
                message="Login successful",
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                },
                status_code=status.HTTP_200_OK,
            )
        except Exception as exception:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message=f"An error occurred: {str(exception)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    async def refresh_token(refresh_token: str) -> APIResponse:
        try:
            payload = jwt.decode(refresh_token, settings.secret_key)
            if payload["type"] != "refresh":
                return APIResponse(
                    status_=StatusEnum.ERROR,
                    message="Invalid token type",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            user_id = int(payload["sub"])
            new_access_token = AuthService.create_access_token(user_id)
            return APIResponse(
                status_=StatusEnum.SUCCESS,
                message="Token refreshed successfully",
                data={
                    "access_token": new_access_token,
                    "token_type": "bearer",
                },
                status_code=status.HTTP_200_OK,
            )
        except jwt.ExpiredTokenError:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Refresh token has expired",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.JoseError:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message="Invalid refresh token",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as exception:
            return APIResponse(
                status_=StatusEnum.ERROR,
                message=f"An error occurred: {str(exception)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def create_access_token(user_id: int) -> str:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode = {"exp": expire, "sub": str(user_id)}
        return jwt.encode(
            {
                "alg": settings.jwt_algorithm,
            },
            to_encode,
            settings.secret_key,
        )

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        expire = datetime.now(UTC) + timedelta(days=settings.refresh_token_expire_days)
        to_encode = {
            "exp": expire,
            "sub": str(user_id),
            "type": "refresh",
        }
        return jwt.encode(
            {"alg": "HS256"},
            to_encode,
            settings.secret_key,
        )
