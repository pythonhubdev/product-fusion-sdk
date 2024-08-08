from product_fusion_backend.dao.base_dao import BaseDAO
from product_fusion_backend.models.member_model import MemberModel


class MemberDAO(BaseDAO[MemberModel]):
    def __init__(self) -> None:
        super().__init__(MemberModel)
