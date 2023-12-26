import crud.base as crud
from sqlalchemy.orm import Session
from models import Student
from schemas.students import StudentSchemaCreate, StudentSchemaUpdate


def create_student(db: Session, schema: StudentSchemaCreate):
    return crud.create_object(db=db, model=Student, schema=schema)


def read_student(db: Session, **kwargs):
    return crud.get_object(db=db, model=Student, **kwargs)


def read_student_by_id(db: Session, student_id: int):
    return crud.get_object_by_id(db=db, model=Student, obj_id=student_id)


def read_students(db: Session, offset: int = 0, limit: int = None, **kwargs):
    return crud.get_all_objects(db=db, model=Student, offset=offset, limit=limit, **kwargs)


def update_student(db: Session, student_id: int, schema: StudentSchemaUpdate):
    return crud.update_object(db=db, obj_id=student_id, model=Student, schema=schema)


def delete_student(db: Session, student_id: int):
    return crud.delete_object(db=db, obj_id=student_id, model=Student)


def delete_all_students(db: Session):
    return crud.delete_all_objects(db=db, model=Student)
