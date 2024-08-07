from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import JSON, BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import BaseModel
from product_fusion_backend.models.organization_model import OrganizationModel

if TYPE_CHECKING:
    from product_fusion_backend.models.organization_model import OrganizationModel


class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)
    profile: Mapped[dict[str, Any]] = mapped_column(JSON, default={}, nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    settings: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, default={})
    created_at: Mapped[Optional[int]] = mapped_column(BigInteger)
    updated_at: Mapped[Optional[int]] = mapped_column(BigInteger)

    organizations: Mapped[list["OrganizationModel"]] = relationship(back_populates="users", secondary="member")
