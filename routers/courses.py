from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

import crud.models.courses as crud
from utils.sockets import notify_clients
from database import get_db
from schemas.courses import CourseSchema, CourseSchemaCreate, CourseSchemaUpdate

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseSchema)
async def create_course(course_schema: CourseSchemaCreate, db: Session = Depends(get_db)):
    course = crud.create_course(db=db, schema=course_schema)
    await notify_clients(f"Создан Курс '{course.title} (ID: {course.id})'")
    return course


@router.get("/", response_model=List[CourseSchema])
async def read_courses(db: Session = Depends(get_db)):
    course = crud.read_courses(db=db)
    return course


@router.get("/", response_model=CourseSchema)
async def read_course(course_id: int, db: Session = Depends(get_db)):
    try:
        course = crud.read_course(db=db, course_id=course_id)
        return course
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course not found")


@router.patch("/", response_model=CourseSchema)
async def update_course(course_id: int, course_schema: CourseSchemaUpdate, db: Session = Depends(get_db)):
    try:
        course = crud.update_course(db=db, course_id=course_id, schema=course_schema)
        await notify_clients(f"Обновлён Курс '{course.title} (ID: {course.id})'")
        return course
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    try:
        course = crud.delete_course(db=db, course_id=course_id)
        await notify_clients(f"Удалён Курс '{course.title} (ID: {course_id})'")
        return course
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Course not found")
