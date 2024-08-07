from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import BaseModel

if TYPE_CHECKING:
    from product_fusion_backend.models.organization_model import OrganizationModel
    from product_fusion_backend.models.role_model import RoleModel
    from product_fusion_backend.models.user_model import UserModel


class MemberModel(BaseModel):
    __tablename__ = "member"

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    settings: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, default={})
    created_at: Mapped[Optional[int]] = mapped_column(BigInteger)
    updated_at: Mapped[Optional[int]] = mapped_column(BigInteger)

    organization: Mapped["OrganizationModel"] = relationship(foreign_keys=[org_id])
    user: Mapped["UserModel"] = relationship(foreign_keys=[user_id])
    role: Mapped["RoleModel"] = relationship(back_populates="members")
