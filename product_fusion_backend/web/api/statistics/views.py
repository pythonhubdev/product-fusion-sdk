from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query

from product_fusion_backend.core import APIResponse
from product_fusion_backend.web.api.statistics.controller import StatsController

stats_router = APIRouter(prefix="/stats", tags=["Statistics"])


@stats_router.get("/role-wise-users")
async def get_role_wise_user_count() -> APIResponse:
    return await StatsController.get_role_wise_user_count()


@stats_router.get("/organization-wise-members")
async def get_organization_wise_member_count() -> APIResponse:
    return await StatsController.get_organization_wise_member_count()


@stats_router.get("/organization-role-wise-users")
async def get_organization_role_wise_user_count(
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    status: Optional[int] = Query(None),
) -> APIResponse:
    return await StatsController.get_organization_role_wise_user_count(from_date, to_date, status)
