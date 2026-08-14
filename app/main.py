from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import todolist, auth, user
from app.config import database
from app.config.database import Base, engine
import app.models
from app.config.secretes import secretes
import jwt
Base.metadata.create_all(bind=engine)

JWT_SECRET_KEY = secretes.JWT_SECRET_KEY
JWT_ALGORITHM = secretes.JWT_ALGORITHM

app = FastAPI()

@app.middleware("http")
async def validateAuth(request, call_next):
    publicRoutes = [
        '/docs',
        '/openapi.json',
        '/redoc',
        '/health',
        '/auth/login',
        '/auth/register',
        '/logout'
    ]
    if request.url.path not in publicRoutes:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
           try: 
              encoded_jwt = auth_header.split(" ", 1)[1]
              decodeJwt=jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
              request.state.userId= decodeJwt["userId"]
           except:
               return JSONResponse(status_code=401, content={
                   'detail': 'Token Expired'
               },)
               
        else:
            return JSONResponse(status_code=401, content={
                'detail': 'Invalid or missing token'
            },)
    response = await call_next(request)
    return response


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(todolist.router)


@app.get("/")
async def read_root():
    return {
        'Hello': 'World'
    }
