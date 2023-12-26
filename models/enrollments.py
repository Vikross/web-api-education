from datetime import datetime
from sqlalchemy import Integer, DateTime, func, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Обратная ссылка на отношение с Course
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    course: Mapped["Course"] = relationship(back_populates="enrollments", lazy="selectin", viewonly=True)

    # Обратная ссылка на отношение с Student
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    student: Mapped["Student"] = relationship(back_populates="enrollments", lazy="selectin", viewonly=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=func.now())
