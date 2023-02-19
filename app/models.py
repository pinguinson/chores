from sqlalchemy import DateTime, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    completions = relationship("Completion", back_populates="user")


class Chore(Base):
    __tablename__ = "chores"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    completions = relationship("Completion", back_populates="chore")


class Completion(Base):
    __tablename__ = "completions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    chore_id = Column(Integer, ForeignKey("chores.id"))
    completed_at = Column(DateTime, index=True)

    chore = relationship("Chore", back_populates="completions")
    user = relationship("User", back_populates="completions")
