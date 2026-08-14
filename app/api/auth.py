from fastapi import APIRouter,Depends
from app.service import auth
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schema.users import CreateUser, UserLogin

router = APIRouter(prefix='/auth', tags=[
    'Authentication'
])


@router.post('/login')
def login(request: UserLogin, db:Session= Depends(get_db)):
    return auth.userLogin(request, db)
    
@router.post('/register')
def registerUser(request: CreateUser, db: Session = Depends(get_db)):
    return auth.registerUser(request, db)

@router.post('/logout')
def logout():   
    return {
        'message': 'Logout successful'
    }   