from fastapi import APIRouter, Depends, Request
from app.service import user
from app.config.database import get_db
from app.schema.users import UserResponse

router = APIRouter(prefix='/user', tags=[
    'User'
])

@router.get('/profile', response_model=UserResponse)
def getUserProfile(request:Request, db = Depends(get_db)):
    info = user.getUserProfileById(db,request.state.userId)
    return info
    

