from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./health.db"

# Create SQLAlchemy engine with SQLite-specific connection args
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()
