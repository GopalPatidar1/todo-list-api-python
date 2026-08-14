from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config.secretes import secretes

if not secretes.DB_URL:
    raise RuntimeError("DB_URL environment variable is not set")

class Base(DeclarativeBase):
    pass

engine = create_engine(
    secretes.DB_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    print("Database connected!")

except Exception as e:
    print(f"Database connection failed: {e}")