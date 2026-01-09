"""Database connection and session management"""
from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def create_tables():
    """Create all tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session
