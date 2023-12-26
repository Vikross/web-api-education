from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class StudentSchemaBase(BaseModel):
    name: str
    email: EmailStr


class StudentSchemaCreate(StudentSchemaBase):
    pass


class StudentSchemaUpdate(StudentSchemaBase):
    name: Optional[str] = None


class StudentSchema(StudentSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
