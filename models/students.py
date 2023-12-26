from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="student", lazy="selectin")

    # Отношение между студентами и курсами (многие ко многим)
    courses: Mapped[List["Course"]] = relationship(secondary='enrollments', back_populates="students", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
