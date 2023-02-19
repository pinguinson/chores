import hashlib
from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    password_hash = hashlib.sha256(user.password.encode("utf-8")).hexdigest()
    db_user = models.User(email=user.email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_chores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chore).offset(skip).limit(limit).all()


def get_chore_by_title(db: Session, title: str):
    return db.query(models.Chore).filter(models.Chore.title == title).all()


def create_chore(db: Session, chore: schemas.ChoreCreate):
    db_chore = models.Chore(**chore.dict())
    db.add(db_chore)
    db.commit()
    db.refresh(db_chore)
    return db_chore


def get_completions(
    db: Session,
    chore_id: int | None = None,
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    filters = make_filter(chore_id=chore_id, user_id=user_id)
    return (
        db.query(models.Completion)
        .filter_by(**filters)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_completion(db: Session, co: schemas.CompletionCreate):
    db_completion = models.Completion(**co.dict(), completed_at=datetime.now())
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion


def make_filter(**kwargs: any) -> dict[str, any]:
    return {k: v for k, v in kwargs.items() if v is not None}
