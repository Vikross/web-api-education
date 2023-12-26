from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EnrollmentSchemaBase(BaseModel):
    course_id: int
    student_id: int


class EnrollmentSchemaCreate(EnrollmentSchemaBase):
    pass


class EnrollmentSchemaUpdate(EnrollmentSchemaBase):
    course_id: Optional[int] = None
    student_id: Optional[int] = None


class EnrollmentSchema(EnrollmentSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
