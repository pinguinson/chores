from fastapi import Cookie, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/chores/", response_model=schemas.Chore)
def create_chore(chore: schemas.ChoreCreate, db: Session = Depends(get_db)):
    db_chore = crud.get_chore_by_title(db, title=chore.title)
    if db_chore:
        raise HTTPException(
            status_code=400, detail="Chore with this title already exists"
        )
    return crud.create_chore(db=db, chore=chore)


@app.get("/chores/", response_model=list[schemas.Chore])
def read_chores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chores = crud.get_chores(db, skip=skip, limit=limit)
    return chores


@app.get("/log/", response_model=list[schemas.Completion])
def read_completions(
    chore_id: int | None = Cookie(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if chore_id:
        return crud.get_completions_by_chore(
            db, chore_id=chore_id, skip=skip, limit=limit
        )
    return crud.get_completions(db, skip=skip, limit=limit)


@app.post("/log/", response_model=schemas.Completion)
def create_completion(
    completion: schemas.CompletionCreate, db: Session = Depends(get_db)
):
    return crud.create_completion(db, co=completion)
