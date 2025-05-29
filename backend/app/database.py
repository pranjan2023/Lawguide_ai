from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use your actual credentials here or better, read from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pratikranjan:Pratik@localhost:5432/Lawguide"
)

# Create the engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is the declarative base that all ORM models will extend
Base = declarative_base()