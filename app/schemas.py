from pydantic import BaseModel
from datetime import datetime


class CompletionBase(BaseModel):
    chore_id: int


class CompletionCreate(CompletionBase):
    user_id: int


class Completion(CompletionBase):
    id: int
    user_id: int
    completed_at: datetime

    class Config:
        orm_mode = True


class ChoreBase(BaseModel):
    title: str


class ChoreCreate(ChoreBase):
    pass


class Chore(ChoreBase):
    id: int
    completions: list[Completion] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    completions: list[Completion] = []

    class Config:
        orm_mode = True
