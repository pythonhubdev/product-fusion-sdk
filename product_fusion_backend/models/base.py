from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, registry

meta = MetaData()


class BaseModel(DeclarativeBase):
    metadata = meta

    registry = registry(
        type_annotation_map={
            datetime: DateTime(timezone=True),
            dict[str, Any]: JSON,
        },
    )
