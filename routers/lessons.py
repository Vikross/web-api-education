from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

import crud.models.lessons as crud
from utils.sockets import notify_clients
from database import get_db
from schemas.lessons import LessonSchema, LessonSchemaCreate, LessonSchemaUpdate

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("/", response_model=LessonSchema)
async def create_lesson(lesson_schema: LessonSchemaCreate, db: Session = Depends(get_db)):
    lesson = crud.create_lesson(db=db, schema=lesson_schema)
    await notify_clients(f"Создан Урок '{lesson.title} (ID: {lesson.id})' в Курсе '{lesson.course.title} (ID: {lesson.course.id})'")
    return lesson


@router.get("/", response_model=List[LessonSchema])
async def read_lessons(db: Session = Depends(get_db)):
    lesson = crud.read_lessons(db=db)
    return lesson


@router.get("/", response_model=LessonSchema)
async def read_lesson(lesson_id: int, db: Session = Depends(get_db)):
    try:
        lesson = crud.read_lesson(db=db, lesson_id=lesson_id)
        return lesson
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Lesson not found")


@router.patch("/", response_model=LessonSchema)
async def update_lesson(lesson_id: int, lesson_schema: LessonSchemaUpdate, db: Session = Depends(get_db)):
    try:
        lesson = crud.update_lesson(db=db, lesson_id=lesson_id, schema=lesson_schema)
        await notify_clients(f"Обновлён Урок '{lesson.title} (ID: {lesson.id})' в Курсе '{lesson.course.title} (ID: {lesson.course.id})'")
        return lesson
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Lesson not found")


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    try:
        lesson = crud.delete_lesson(db=db, lesson_id=lesson_id)
        await notify_clients(f"Удалён Урок '{lesson.title} (ID: {lesson.id})' в Курсе '{lesson.course.title} (ID: {lesson.course.id})'")
        return lesson
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Lesson not found")
