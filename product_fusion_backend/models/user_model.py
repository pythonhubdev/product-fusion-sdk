from typing import Any

from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import Base, BaseModel


class UserModel(BaseModel, Base):
    __tablename__ = "user"  # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    profile: Mapped[dict[Any, Any]] = mapped_column(JSON, default={}, nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    settings: Mapped[dict[Any, Any]] = mapped_column(JSON, default={}, nullable=True)

    organizations = relationship(
        "OrganizationModel",
        secondary="member",
        back_populates="users",
        overlaps="members,organization,user",
    )
    members = relationship("MemberModel", back_populates="user", overlaps="organizations,user")
