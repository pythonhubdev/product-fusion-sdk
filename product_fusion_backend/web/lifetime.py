from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from product_fusion_backend.core import OpenTelemetry
from product_fusion_backend.database import database
from product_fusion_backend.models.base import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.middleware_stack = None
    OpenTelemetry.setup_opentelemetry(app)
    app.middleware_stack = app.build_middleware_stack()
    async with database.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    OpenTelemetry.stop_opentelemetry(app)
