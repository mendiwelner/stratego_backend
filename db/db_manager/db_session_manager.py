from db.db_manager.database import SessionLocal
from sqlalchemy.orm import Session


class DBSessionManager:
    @staticmethod
    def get_db() -> Session:
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()
