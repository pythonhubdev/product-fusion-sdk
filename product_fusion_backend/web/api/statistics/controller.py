from datetime import datetime
from typing import Optional

from product_fusion_backend.core import APIResponse, StatusEnum
from product_fusion_backend.dao import OrganizationDAO, RoleDAO


class StatsController:
    @staticmethod
    async def get_role_wise_user_count() -> APIResponse:
        stats = await RoleDAO().get_role_wise_user_count()  # type: ignore
        return APIResponse(
            status_=StatusEnum.SUCCESS,
            message="Role-wise user count retrieved successfully",
            data=stats,
            status_code=200,
        )

    @staticmethod
    async def get_organization_wise_member_count() -> APIResponse:
        stats = await OrganizationDAO().get_organization_wise_member_count()  # type: ignore
        return APIResponse(
            status_=StatusEnum.SUCCESS,
            message="Organization-wise member count retrieved successfully",
            data=stats,
            status_code=200,
        )

    @staticmethod
    async def get_organization_role_wise_user_count(
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        status: Optional[int] = None,
    ) -> APIResponse:
        stats = await OrganizationDAO().get_organization_role_wise_user_count(  # type: ignore
            from_date,
            to_date,
            status,
        )
        return APIResponse(
            status_=StatusEnum.SUCCESS,
            message="Organization and role-wise user count retrieved successfully",
            data=stats,
            status_code=200,
        )
