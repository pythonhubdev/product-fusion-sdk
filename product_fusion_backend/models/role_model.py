from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import BaseModel

if TYPE_CHECKING:
    from product_fusion_backend.models.member_model import MemberModel
    from product_fusion_backend.models.organization_model import OrganizationModel


class RoleModel(BaseModel):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    org_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)

    organization: Mapped["OrganizationModel"] = relationship(back_populates="roles")
    members: Mapped[list["MemberModel"]] = relationship(back_populates="role")
