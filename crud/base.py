from pydantic import BaseModel as SchemaBase
from sqlalchemy.orm import Session

from database import Base as ModelBase


def create_object(db: Session, model: ModelBase, schema: SchemaBase, **kwargs):
    obj_data = schema.model_dump()
    obj_data.update(kwargs)
    obj = model(**obj_data)

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


def get_object(db: Session, model: ModelBase, **kwargs):
    return filter_objects(db=db, model=model, **kwargs).first()


def get_object_by_id(db: Session, model: ModelBase, obj_id: int):
    return filter_objects(db=db, model=model, id=obj_id).first()


def get_all_objects(db: Session, model: ModelBase, offset: int = 0, limit: int = None, **kwargs):
    if kwargs:
        query = filter_objects(db=db, model=model, **kwargs).offset(offset)
    else:
        query = db.query(model).offset(offset)

    if limit is not None:
        query = query.limit(limit)
    return query.all()


def filter_objects(db: Session, model: ModelBase, **kwargs):
    valid_attributes = [attr for attr in kwargs.keys() if hasattr(model, attr)]
    filters = [getattr(model, attr) == value for attr, value in kwargs.items() if attr in valid_attributes]
    return db.query(model).filter(*filters)


def update_object(db: Session, obj_id: int, model: ModelBase, schema: SchemaBase):
    db_obj = get_object_by_id(db=db, model=model, obj_id=obj_id)

    for var, value in vars(schema).items():
        setattr(db_obj, var, value) if value or str(value) == 'False' else None

    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_object(db: Session, obj_id: int, model: ModelBase):
    db_obj = get_object_by_id(db=db, model=model, obj_id=obj_id)
    db.delete(db_obj)
    db.commit()
    return db_obj


def delete_all_objects(db: Session, model: ModelBase):
    db.query(model).delete()
    db.commit()
    return True
