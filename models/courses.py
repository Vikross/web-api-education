from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)

    # Отношение между курсами и уроками (один ко многим)
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="course", lazy="selectin", cascade="all, delete")

    # Отношение между курсами и студентами (многие ко многим)
    students: Mapped[List["Student"]] = relationship(
        "Student",
        secondary='enrollments',
        back_populates="courses",
        lazy="selectin",
        viewonly=True
    )

    enrollments: Mapped[List["Enrollment"]] = relationship(back_populates="course", lazy="selectin", cascade="all, delete", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
