import asyncio

from fastapi import FastAPI
from hypercorn.asyncio import serve
from loguru import logger

from product_fusion_backend.core import configure_logging
from product_fusion_backend.server_config import HypercornConfig


class HypercornApplication:
    """
    Custom Hypercorn application.

    This class is used to start Hypercorn with the FastAPI application.
    """

    def __init__(
        self,
        app: FastAPI,
    ) -> None:
        self.app = app
        configure_logging()

    def run(self) -> None:
        """
        Run the FastAPI application with Hypercorn.
        """
        config = HypercornConfig()
        logger.info("Configuring Hypercorn Server...")
        logger.info(f"Starting Hypercorn Server on http://{config.bind[0]}")
        asyncio.run(serve(self.app, config))  # type: ignore
