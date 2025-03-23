from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
# from backend.db.db_models.base import Base
# from backend.db.db_models.game import Game
# from backend.db.db_models.user import User
from db.db_models.base import Base
from db.db_models.game import Game
from db.db_models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./stratego.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
# הצגת הטבלאות והעמודות שלהן
inspector = inspect(engine)
for table_name in inspector.get_table_names():
    print(f"Table: {table_name}")
    columns = inspector.get_columns(table_name)
    for column in columns:
        print(f"  Column: {column['name']} - Type: {column['type']}")