from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from product_fusion_backend.connections import inject_session
from product_fusion_backend.dao.base_dao import BaseDAO
from product_fusion_backend.models.user_model import UserModel


class UserDAO(BaseDAO[UserModel]):
    def __init__(self) -> None:
        super().__init__(UserModel)

    @inject_session
    async def get_by_email(self, email: str, session: AsyncSession) -> Optional[UserModel]:
        statement = select(self.model).where(
            self.model.email == email,  # noqa
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @inject_session
    async def get_by_reset_token(self, token: str, session: AsyncSession) -> Optional[UserModel]:
        token = token.strip()
        statement = select(self.model).where(
            (self.model.settings["reset_token"].op("->>")("token") == token),  # noqa
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @inject_session
    async def get_by_verification_token(self, token: str, session: AsyncSession) -> Optional[UserModel]:
        statement = select(self.model).where(
            self.model.settings["email_verification"].op("->>")("token") == token,  # noqa
        )
        result = await session.execute(statement)
        return result.scalars().first()
