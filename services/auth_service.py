from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.db_crud.user_crud import UserCRUD
from services.auth_manager import AuthManager
from fastapi.security import OAuth2PasswordRequestForm


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, form_data: OAuth2PasswordRequestForm):
        user = UserCRUD.get_user_by_name(db, form_data.username)
        if not user or user.password != form_data.password:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = AuthManager.create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
