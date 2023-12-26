import crud.base as crud
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Enrollment
from schemas.enrollments import EnrollmentSchemaCreate, EnrollmentSchemaUpdate


def create_enrollment(db: Session, schema: EnrollmentSchemaCreate):
    if crud.get_object(db=db, model=Enrollment, course_id=schema.course_id, student_id=schema.student_id):
        raise IntegrityError  # "course_id and student_id must be UNIQUE"
    return crud.create_object(db=db, model=Enrollment, schema=schema)


def read_enrollment(db: Session, **kwargs):
    return crud.get_object(db=db, model=Enrollment, **kwargs)


def read_enrollment_by_id(db: Session, enrollment_id: int):
    return crud.get_object_by_id(db=db, model=Enrollment, obj_id=enrollment_id)


def read_enrollments(db: Session, offset: int = 0, limit: int = None, **kwargs):
    return crud.get_all_objects(db=db, model=Enrollment, offset=offset, limit=limit, **kwargs)


def update_enrollment(db: Session, enrollment_id: int, schema: EnrollmentSchemaUpdate):
    return crud.update_object(db=db, obj_id=enrollment_id, model=Enrollment, schema=schema)


def delete_enrollment(db: Session, enrollment_id: int):
    return crud.delete_object(db=db, obj_id=enrollment_id, model=Enrollment)


def delete_all_enrollments(db: Session):
    return crud.delete_all_objects(db=db, model=Enrollment)
