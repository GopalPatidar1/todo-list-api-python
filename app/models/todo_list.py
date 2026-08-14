from sqlalchemy import Column, String
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base

class TodoStatus(str, Enum):
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

class TodoList(Base):
    __tablename__ = "todo_list"
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(255), nullable=False)
    desc: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[TodoStatus] = mapped_column(SQLEnum(TodoStatus), default=TodoStatus.INCOMPLETE, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="todos"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)