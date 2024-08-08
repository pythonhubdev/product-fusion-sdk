from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import Base, BaseModel


class MemberModel(BaseModel, Base):
    __tablename__ = "member"  # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    settings: Mapped[dict[Any, Any]] = mapped_column(JSON, default={}, nullable=True)

    organization = relationship("OrganizationModel", back_populates="members")
    user = relationship("UserModel", back_populates="members")
    role = relationship("RoleModel", back_populates="members")
