import crud.base as crud
from sqlalchemy.orm import Session
from models import Lesson
from schemas.lessons import LessonSchemaCreate, LessonSchemaUpdate


def create_lesson(db: Session, schema: LessonSchemaCreate):
    return crud.create_object(db=db, model=Lesson, schema=schema)


def read_lesson(db: Session, **kwargs):
    return crud.get_object(db=db, model=Lesson, **kwargs)


def read_lesson_by_id(db: Session, lesson_id: int):
    return crud.get_object_by_id(db=db, model=Lesson, obj_id=lesson_id)


def read_lessons(db: Session, offset: int = 0, limit: int = None, **kwargs):
    return crud.get_all_objects(db=db, model=Lesson, offset=offset, limit=limit, **kwargs)


def update_lesson(db: Session, lesson_id: int, schema: LessonSchemaUpdate):
    return crud.update_object(db=db, obj_id=lesson_id, model=Lesson, schema=schema)


def delete_lesson(db: Session, lesson_id: int):
    return crud.delete_object(db=db, obj_id=lesson_id, model=Lesson)


def delete_all_lessons(db: Session):
    return crud.delete_all_objects(db=db, model=Lesson)
