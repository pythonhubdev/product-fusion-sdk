from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from product_fusion_backend.core.utils.enums import StatusEnum


class CommonResponseSchema(BaseModel):
    status: StatusEnum
    message: str
    data: Optional[dict[Any, Any] | list[dict[Any, Any]]] = None
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "message": "The project is healthy.",
            },
        },
    )
