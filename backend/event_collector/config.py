"""
config.py is the file that contains the configuration.
"""

import os
import dotenv

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from models import Base

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    if not tables:
        print("No tables created.")
    else:
        print(f"Tables created: {tables}")
