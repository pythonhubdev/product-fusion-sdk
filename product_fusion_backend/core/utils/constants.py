from typing import Type, TypedDict

from pydantic import BaseModel

from product_fusion_backend.core.schema.common_response_schema import CommonResponseSchema


class RouteOptions(TypedDict):
    response_model_exclude_none: bool
    response_model: Type[BaseModel]


DEFAULT_ROUTE_OPTIONS: RouteOptions = {
    "response_model_exclude_none": True,
    "response_model": CommonResponseSchema,
}
