from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CourseSchemaBase(BaseModel):
    title: str
    description: str


class CourseSchemaCreate(CourseSchemaBase):
    pass


class CourseSchemaUpdate(CourseSchemaBase):
    title: Optional[str] = None
    description: Optional[str] = None


class CourseSchema(CourseSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
