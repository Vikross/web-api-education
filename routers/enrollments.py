from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

import crud.models.enrollments as crud
from utils.sockets import notify_clients
from database import get_db
from schemas.enrollments import EnrollmentSchema, EnrollmentSchemaCreate, EnrollmentSchemaUpdate

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


@router.post("/", response_model=EnrollmentSchema)
async def create_enrollment(enrollment_schema: EnrollmentSchemaCreate, db: Session = Depends(get_db)):
    if crud.read_enrollment(db=db, student_id=enrollment_schema.student_id, course_id=enrollment_schema.course_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="The record already exists. The student_id and course_id in the bundle should be used only once.")
    enrollment = crud.create_enrollment(db=db, schema=enrollment_schema)
    await notify_clients(f"Создано Зачисление (ID: {enrollment.id}) студента '{enrollment.student.name} (ID: {enrollment.student_id})' "
                         f"на курс '{enrollment.course.title} (ID: {enrollment.course.id})'")
    return enrollment


@router.get("/", response_model=List[EnrollmentSchema])
async def read_enrollments(db: Session = Depends(get_db)):
    enrollment = crud.read_enrollments(db=db)
    return enrollment


@router.get("/", response_model=EnrollmentSchema)
async def read_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        enrollment = crud.read_enrollment(db=db, enrollment_id=enrollment_id)
        return enrollment
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Enrollment not found")


@router.patch("/", response_model=EnrollmentSchema)
async def update_enrollment(enrollment_id: int, enrollment_schema: EnrollmentSchemaUpdate, db: Session = Depends(get_db)):
    try:
        enrollment = crud.update_enrollment(db=db, enrollment_id=enrollment_id, schema=enrollment_schema)
        await notify_clients(f"Обновлено Зачисление (ID: {enrollment.id}) студента '{enrollment.student.name} (ID: {enrollment.student_id})' "
                             f"на Курс '{enrollment.course.title} (ID: {enrollment.course.id})'")
        return enrollment
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Enrollment not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    try:
        enrollment = crud.delete_enrollment(db=db, enrollment_id=enrollment_id)
        await notify_clients(f"Удалено Зачисление (ID: {enrollment.id}) студента '{enrollment.student.name} (ID: {enrollment.student_id})' "
                             f"с Курса  '{enrollment.course.title} (ID: {enrollment.course.id})'")
        return enrollment
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Enrollment not found")

