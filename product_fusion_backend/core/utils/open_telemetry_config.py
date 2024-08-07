from fastapi import FastAPI
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import DEPLOYMENT_ENVIRONMENT, SERVICE_NAME, TELEMETRY_SDK_LANGUAGE, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider

from product_fusion_backend.settings import settings


class OpenTelemetry:
    @staticmethod
    def setup_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
        """
        Enables opentelemetry instrumentation.

        :param app: current application.
        """
        if not settings.opentelemetry_endpoint:
            return

        tracer_provider = TracerProvider(
            resource=Resource(
                attributes={
                    SERVICE_NAME: "product_fusion_backend",
                    TELEMETRY_SDK_LANGUAGE: "python",
                    DEPLOYMENT_ENVIRONMENT: settings.environment,
                },
            ),
        )

        tracer_provider.add_span_processor(
            BatchSpanProcessor(
                OTLPSpanExporter(
                    endpoint=settings.opentelemetry_endpoint,
                    insecure=True,
                ),
            ),
        )

        excluded_endpoints = [
            app.url_path_for("health_check"),
            app.url_path_for("openapi"),
            app.url_path_for("swagger_ui_html"),
            app.url_path_for("swagger_ui_redirect"),
            app.url_path_for("redoc_html"),
        ]

        FastAPIInstrumentor().instrument_app(
            app,
            tracer_provider=tracer_provider,
            excluded_urls=",".join(excluded_endpoints),
        )

        set_tracer_provider(tracer_provider=tracer_provider)

    @staticmethod
    def stop_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
        """
        Disables opentelemetry instrumentation.

        :param app: current application.
        """
        if not settings.opentelemetry_endpoint:
            return

        FastAPIInstrumentor().uninstrument_app(app)
