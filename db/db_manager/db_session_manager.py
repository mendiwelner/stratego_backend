from db.db_manager.database import SessionLocal


class DBSessionManager:
    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
