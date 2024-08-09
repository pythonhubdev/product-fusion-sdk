from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from product_fusion_backend.connections import inject_session
from product_fusion_backend.dao.base_dao import BaseDAO
from product_fusion_backend.models import MemberModel
from product_fusion_backend.models.role_model import RoleModel


class RoleDAO(BaseDAO[RoleModel]):
    def __init__(self) -> None:
        super().__init__(RoleModel)

    @inject_session
    async def get_by_name_and_org(self, name: str, org_id: int, session: AsyncSession) -> Optional[RoleModel]:
        statement = select(self.model).where(
            self.model.name == name,  # noqa
            self.model.org_id == org_id,  # noqa
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @inject_session
    async def get_role_wise_user_count(self, session: AsyncSession) -> list[dict[str, Any]]:
        member = aliased(MemberModel)
        statement = (
            select(
                self.model.name.label("role"),
                func.count(member.user_id.distinct()).label("user_count"),  # noqa
            )
            .join(member, self.model.id == member.role_id)  # noqa
            .group_by(self.model.name)
        )
        result = await session.execute(statement)
        return [{"role": row.role, "user_count": row.user_count} for row in result]
