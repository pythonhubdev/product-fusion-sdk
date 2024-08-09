from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from product_fusion_backend.connections import inject_session
from product_fusion_backend.dao.base_dao import BaseDAO
from product_fusion_backend.models.member_model import MemberModel


class MemberDAO(BaseDAO[MemberModel]):
    def __init__(self) -> None:
        super().__init__(MemberModel)

    @inject_session
    async def get_by_user_and_org(
        self,
        user_id: int,
        org_id: int,
        session: AsyncSession,
    ) -> Optional[MemberModel]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.role))
            .where(
                and_(
                    (self.model.user_id == int(user_id)),
                    (self.model.org_id == int(org_id)),
                ),
            )
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @inject_session
    async def get_user_with_role(
        self,
        member_id: int,
        session: AsyncSession,
    ) -> Optional[MemberModel]:
        statement = (
            select(self.model)
            .options(selectinload(self.model.role))
            .where(
                (self.model.id == int(member_id)),  # noqa
            )
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @inject_session
    async def get_by_invite_token(self, token: str, session: AsyncSession) -> Optional[MemberModel]:
        token = token.strip()
        statement = (
            select(self.model)
            .options(selectinload(self.model.role))
            .where(self.model.settings["invite_token"].op("->>")("token") == token)  # noqa
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @inject_session
    async def count_by_role_in_org(self, role_name: str, org_id: int, session: AsyncSession) -> int:
        statement = (
            select(func.count())
            .select_from(self.model)
            .join(self.model.role)
            .where((self.model.org_id == org_id) & (self.model.role.has(name=role_name)))
        )
        result = await session.execute(statement)
        return result.scalar_one()
