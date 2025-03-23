from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db_models.user import User


class UserCRUD:
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def create_user(db: Session, name: str, password: str):
        existing_user = db.query(User).filter(User.name == name).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Address already exists!")

        new_user = User(name=name, password=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_name(db: Session, name: str):
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": f"User {user_id} deleted successfully"}

    @staticmethod
    def delete_all_users(db: Session):
        try:
            db.query(User).delete()
            db.commit()
            return {"message": "All users have been deleted successfully"}
        except Exception as e:
            db.rollback()
            return {"message": f"Error occurred: {str(e)}"}

