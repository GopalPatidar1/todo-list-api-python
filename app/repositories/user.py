from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.users import User

def createUser(db:Session, user):
    db.add(user)
    db.flush()

def getUserByEmail(db:Session , email:str):
     return db.scalar(
        select(User).where(User.email == email)
    )

def getUserById(db: Session, id: str):
     return db.scalar(
          select(User).where(User.id == int(id))
     )