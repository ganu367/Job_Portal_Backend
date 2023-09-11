from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import dotenv_values
from dotenv import load_dotenv

config = dotenv_values(".env")
connect = load_dotenv()

# defining postgres sql database
# SQLALCHEMY_DATABASE_URL = os.getenv('POSTGRES_URL')

# engine = create_engine(SQLALCHEMY_DATABASE_URL,
#                        execution_options={
#                            "isolation_level": "REPEATABLE READ"})

SQLALCHEMY_DATABASE_URL = "sqlite:///./job_portal.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# getting database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
