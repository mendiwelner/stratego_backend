from typing import List, Type
from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db_models.user import User


class UserCRUD:
    @staticmethod
    def get_user(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session) -> List[Type[User]]:
        return db.query(User).all()

    @staticmethod
    def create_user(db: Session, name: str, password: str, setup: str, is_active: bool) -> User:
        existing_user = db.query(User).filter(User.name == name).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Address already exists!")
        new_user = User(name=name, password=password, setup=setup, rating=1500, is_active=is_active)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user_by_name(db: Session, name: str) -> User | None:
        return db.query(User).filter(User.name == name).first()

    @staticmethod
    def delete_user(db: Session, user_id: int) -> dict:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": f"User {user_id} deleted successfully"}

    @staticmethod
    def delete_all_users(db: Session) -> dict:
        try:
            db.query(User).delete()
            db.commit()
            return {"message": "All users have been deleted successfully"}
        except Exception as e:
            db.rollback()
            return {"message": f"Error occurred: {str(e)}"}

    @staticmethod
    def update_user_rating(db: Session, user_name: str, new_rating: int) -> dict:
        user = db.query(User).filter(User.name == user_name).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.rating = new_rating
        db.commit()
        db.refresh(user)
        return {"message": "User rating updated successfully", "user_name": user_name, "new_rating": new_rating}

    @staticmethod
    def update_user_activity(db: Session, user_name: str, is_active: bool) -> dict:
        user = db.query(User).filter(User.name == user_name).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_active = is_active
        db.commit()
        db.refresh(user)
        return {"message": "User activity updated successfully", "user_name": user_name, "activity": is_active}

    @staticmethod
    def get_active_users_count(db: Session) -> dict:
        active_users_count = db.query(User).filter(User.is_active).count()
        return {"active_users_count": active_users_count}
