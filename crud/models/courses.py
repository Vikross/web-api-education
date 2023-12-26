import crud.base as crud
from sqlalchemy.orm import Session
from models import Course
from schemas.courses import CourseSchemaCreate, CourseSchemaUpdate


def create_course(db: Session, schema: CourseSchemaCreate):
    return crud.create_object(db=db, model=Course, schema=schema)


def read_course(db: Session, **kwargs):
    return crud.get_object(db=db, model=Course, **kwargs)


def read_course_by_id(db: Session, course_id: int):
    return crud.get_object_by_id(db=db, model=Course, obj_id=course_id)


def read_courses(db: Session, offset: int = 0, limit: int = None, **kwargs):
    return crud.get_all_objects(db=db, model=Course, offset=offset, limit=limit, **kwargs)


def update_course(db: Session, course_id: int, schema: CourseSchemaUpdate):
    return crud.update_object(db=db, obj_id=course_id, model=Course, schema=schema)


def delete_course(db: Session, course_id: int):
    return crud.delete_object(db=db, obj_id=course_id, model=Course)


def delete_all_courses(db: Session):
    return crud.delete_all_objects(db=db, model=Course)
