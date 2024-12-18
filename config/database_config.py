from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
DATABASE_URL = "postgresql://postgres:toor@localhost:5432/StoreManagerDatabase"

# Create a Database instance
database = Database(DATABASE_URL)

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autoflush=False, autocommit=False, bind=engine
)


def db_init() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
