import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from product_fusion_backend.connections import database
from product_fusion_backend.core import OpenTelemetry, redis_service
from product_fusion_backend.models.base import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.middleware_stack = None
    OpenTelemetry.setup_opentelemetry(app)
    app.middleware_stack = app.build_middleware_stack()
    await redis_service.start_subscriber("email-channel")
    async with database.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    await redis_service.stop_subscriber()
    OpenTelemetry.stop_opentelemetry(app)
