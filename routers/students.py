from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

import crud.models.students as crud
from utils.sockets import notify_clients
from database import get_db
from schemas.students import StudentSchema, StudentSchemaCreate, StudentSchemaUpdate

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=StudentSchema)
async def create_student(student_schema: StudentSchemaCreate, db: Session = Depends(get_db)):
    if crud.read_student(db=db, email=student_schema.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Студент с такой почтой уже существует.")

    student = crud.create_student(db=db, schema=student_schema)
    await notify_clients(f"Создан Студент '{student.name} | {student.email} (ID: {student.id})'")
    return student


@router.get("/", response_model=List[StudentSchema])
async def read_students(db: Session = Depends(get_db)):
    student = crud.read_students(db=db)
    return student


@router.get("/", response_model=StudentSchema)
async def read_student(student_id: int, db: Session = Depends(get_db)):
    try:
        student = crud.read_student(db=db, student_id=student_id)
        return student
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Student not found")


@router.patch("/", response_model=StudentSchema)
async def update_student(student_id: int, student_schema: StudentSchemaUpdate, db: Session = Depends(get_db)):
    student = crud.update_student(db=db, student_id=student_id, schema=student_schema)
    try:
        await notify_clients(f"Обновлён Студент '{student.name} | {student.email} (ID: {student.id})'")
        return student
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Student not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    try:
        student = crud.delete_student(db=db, student_id=student_id)
        await notify_clients(f"Удалён Студент '{student.name} | {student.email} (ID: {student.id})'")
        return student
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Student not found")

