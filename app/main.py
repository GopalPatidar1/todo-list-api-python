from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import todolist, auth, user
from app.config import database
from app.config.database import Base, engine
import app.models
from app.config.secretes import secretes
import jwt
from app.core.customException import CustomException
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

JWT_SECRET_KEY = secretes.JWT_SECRET_KEY
JWT_ALGORITHM = secretes.JWT_ALGORITHM

app = FastAPI(lifespan=lifespan)

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
              decodeJwt = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
              request.state.userId = int(decodeJwt["userId"])
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

# import anyio
# import anyio.to_thread
# limiter = anyio.to_thread.current_default_thread_limiter()
# print("🚀 ~ limiter:", limiter.total_tokens)
# print("🚀 ~ limiter:", limiter.borrowed_tokens)

@app.get("/health")
async def read_root():
    # await anyio.sleep(2)
    return {
        'Hello': 'World'
    }

@app.exception_handler(CustomException)
async def global_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': exc.message
        }
    )