from datetime import datetime
from typing import Any, Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from product_fusion_backend.connections import inject_session
from product_fusion_backend.dao.base_dao import BaseDAO
from product_fusion_backend.models import MemberModel, RoleModel, UserModel
from product_fusion_backend.models.organization_model import OrganizationModel


class OrganizationDAO(BaseDAO[OrganizationModel]):
    def __init__(self) -> None:
        super().__init__(OrganizationModel)

    @inject_session
    async def get_by_name(self, name: str, session: AsyncSession) -> Optional[OrganizationModel]:
        statement = select(self.model).where(
            self.model.name == name,  # noqa
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @inject_session
    async def get_organization_wise_member_count(self, session: AsyncSession) -> list[dict[str, Any]]:
        member = aliased(MemberModel)
        statement = (
            select(
                self.model.name.label("organization"),
                func.count(member.user_id.distinct()).label("member_count"),  # noqa
            )
            .join(member, self.model.id == member.org_id)  # noqa
            .group_by(self.model.name)
        )
        result = await session.execute(statement)
        return [{"organization": row.organization, "member_count": row.member_count} for row in result]

    @inject_session
    async def get_organization_role_wise_user_count(
        self,
        from_date: Optional[datetime],
        to_date: Optional[datetime],
        status: Optional[int],
        session: AsyncSession,
    ) -> list[dict[str, Any]]:
        role = aliased(RoleModel)
        member = aliased(MemberModel)
        user = aliased(UserModel)

        statement = (
            select(
                self.model.name.label("organization"),
                role.name.label("role"),  # noqa
                func.count(member.user_id.distinct()).label("user_count"),  # noqa
            )
            .join(member, self.model.id == member.org_id)  # noqa
            .join(role, member.role_id == role.id)
            .join(user, member.user_id == user.id)
        )

        conditions = []
        if from_date:
            conditions.append(member.created_at >= from_date)
        if to_date:
            conditions.append(member.created_at <= to_date)
        if status is not None:
            conditions.append(member.status == status)

        if conditions:
            statement = statement.where(and_(*conditions))

        statement = statement.group_by(self.model.name, role.name)

        result = await session.execute(statement)
        return [
            {
                "organization": row.organization,
                "role": row.role,
                "user_count": row.user_count,
            }
            for row in result
        ]
