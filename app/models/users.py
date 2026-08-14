from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, func, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase ,Mapped, mapped_column, relationship
from app.config.database import Base

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(30), nullable=False)
    lastname: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(30))
    status: Mapped[UserStatus] = mapped_column(SQLEnum(UserStatus), default=UserStatus.ACTIVE, nullable=False)

    todos: Mapped[list["TodoList"]] = relationship(
        back_populates="user"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True,)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, lastname={self.lastname!r}, email={self.email!r})"