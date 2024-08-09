from fastapi import APIRouter

from product_fusion_backend.web.api.auth import auth_router
from product_fusion_backend.web.api.docs import docs_router
from product_fusion_backend.web.api.member import org_member_router
from product_fusion_backend.web.api.monitoring import health_router
from product_fusion_backend.web.api.statistics import stats_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(docs_router)
api_router.include_router(auth_router)
api_router.include_router(org_member_router)
api_router.include_router(stats_router)
