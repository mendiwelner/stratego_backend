from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db_models.base import Base
from db.db_models.game import Game
from db.db_models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./stratego.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# יצירת טבלאות
Base.metadata.create_all(bind=engine)
print(Base.metadata.tables.keys())
