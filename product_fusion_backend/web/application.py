from importlib import metadata
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from product_fusion_backend.core import DEFAULT_ROUTE_OPTIONS, CommonResponseSchema, StatusEnum, configure_logging
from product_fusion_backend.middlewares import JWTAuthMiddleware, LoggingMiddleware
from product_fusion_backend.web.api.router import api_router
from product_fusion_backend.web.lifetime import lifespan

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="Product Fusion Backend",
        version=metadata.version("product_fusion_backend"),
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)  # type: ignore
    app.add_middleware(JWTAuthMiddleware)  # type: ignore

    app.include_router(router=api_router, prefix="/api")

    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    @app.get("/", tags=["Root"], **DEFAULT_ROUTE_OPTIONS)
    def read_root() -> CommonResponseSchema:
        return CommonResponseSchema(
            status=StatusEnum.SUCCESS,
            message="Welcome to Product Fusion Backend!!",
            data={
                "ping": "pong",
            },
        )

    configure_logging()
    return app


pf_app: FastAPI = get_app()
