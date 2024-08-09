from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from product_fusion_backend.models.base import Base, BaseModel


class RoleModel(BaseModel, Base):
    __tablename__ = "role"  # type: ignore

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)

    organization = relationship("OrganizationModel", back_populates="roles")
    members = relationship("MemberModel", back_populates="role")
