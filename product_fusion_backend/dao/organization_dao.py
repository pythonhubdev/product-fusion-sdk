from typing import Optional

from sqlalchemy import ColumnElement, select
from sqlalchemy.ext.asyncio import AsyncSession

from product_fusion_backend.connections import inject_session
from product_fusion_backend.dao.base_dao import BaseDAO
from product_fusion_backend.models.organization_model import OrganizationModel


class OrganizationDAO(BaseDAO[OrganizationModel]):
    def __init__(self) -> None:
        super().__init__(OrganizationModel)

    @inject_session
    async def get_by_name(self, name: str, session: AsyncSession) -> Optional[OrganizationModel]:
        statement = select(self.model).where(
            ColumnElement[bool],
            self.model.name == name,  # noqa
        )
        result = await session.execute(statement)
        return result.scalars().first()
