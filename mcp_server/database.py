from sqlmodel import create_engine, Session, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment variables")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Database session dependency
def get_session():
    with Session(engine) as session:
        yield session