from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON, BigInteger, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import BaseModel

if TYPE_CHECKING:
    from product_fusion_backend.models.role_model import RoleModel
    from product_fusion_backend.models.user_model import UserModel


class OrganizationModel(BaseModel):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    personal: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    settings: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, default={})
    created_at: Mapped[Optional[int]] = mapped_column(BigInteger)
    updated_at: Mapped[Optional[int]] = mapped_column(BigInteger)

    users: Mapped[list["UserModel"]] = relationship(back_populates="organizations", secondary="member")
    roles: Mapped[list["RoleModel"]] = relationship(back_populates="organization")
