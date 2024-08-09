from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from product_fusion_backend.connections import inject_session
from product_fusion_backend.dao.base_dao import BaseDAO
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
