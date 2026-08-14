from app.models.users import User
from app.repositories import user as userRepo
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
import os
import jwt

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def registerUser(request, db):
    try:
      user = User(
          firstname=request.firstname,
          lastname=request.lastname,
          email=request.email,
          password=request.password
      )
      
      userRepo.createUser(db, user)

      db.commit()
      db.refresh(user)
      
      return {
          "id": user.id,
          "name": user.firstname,
          "email": user.email
      }
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code = 500,content={
            'detail': 'Something went wrong'
        })

def createAccessToken(userId: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = { "userId": str(userId), "exp": expire }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

def userLogin(request, db):
   user = userRepo.getUserByEmail(db, request.email)
   if not user or user.password != request.password:
     raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Incorrect email or password",
     )
   return createAccessToken(user.id)