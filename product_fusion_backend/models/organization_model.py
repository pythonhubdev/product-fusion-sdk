from typing import Any

from sqlalchemy import JSON, BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import Base, BaseModel


class OrganizationModel(BaseModel, Base):
    __tablename__ = "organization"  # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    personal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    settings: Mapped[dict[Any, Any]] = mapped_column(JSON, default={}, nullable=True)

    users = relationship(
        "UserModel",
        secondary="member",
        back_populates="organizations",
        overlaps="members,organization,user",
    )
    roles = relationship("RoleModel", back_populates="organization")
    members = relationship("MemberModel", back_populates="organization", overlaps="users,organization")
