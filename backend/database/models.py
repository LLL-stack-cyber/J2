from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    notes: Mapped[list["StudyNote"]] = relationship(back_populates="owner", cascade="all, delete-orphan")
    exam_results: Mapped[list["ExamResult"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class StudyNote(Base):
    __tablename__ = "study_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped[User] = relationship(back_populates="notes")


class ExamResult(Base):
    __tablename__ = "exam_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    topic: Mapped[str] = mapped_column(String(255), index=True)
    score: Mapped[float] = mapped_column(Float)
    feedback: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped[User] = relationship(back_populates="exam_results")
