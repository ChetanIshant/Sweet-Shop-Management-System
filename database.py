import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

def init_db():
    SQLModel.metadata.create_all(engine)
    # Ensure any missing columns from model changes are added for simple dev setups.
    # SQLite supports adding columns via ALTER TABLE; this makes local dev easier
    # without a full migration tool. Only add `is_verified` if it doesn't exist.
    if engine.url.scheme.startswith("sqlite"):
        with engine.connect() as conn:
            insp = conn.execute(text("PRAGMA table_info('user')")).fetchall()
            cols = {row[1] for row in insp}
            if "is_verified" not in cols:
                conn.execute(text("ALTER TABLE user ADD COLUMN is_verified BOOLEAN NOT NULL DEFAULT 0"))

def get_session():
    with Session(engine) as s:
        yield s