from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LessonSchemaBase(BaseModel):
    title: str
    content: str
    course_id: int


class LessonSchemaCreate(LessonSchemaBase):
    pass


class LessonSchemaUpdate(LessonSchemaBase):
    title: Optional[str] = None
    content: Optional[str] = None
    course_id: Optional[int] = None


class LessonSchema(LessonSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
