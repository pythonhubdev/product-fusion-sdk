from fastapi import APIRouter

from product_fusion_backend.web.api.auth import auth_router
from product_fusion_backend.web.api.docs import docs_router
from product_fusion_backend.web.api.monitoring import health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(docs_router)
api_router.include_router(auth_router)
