from sqlalchemy.orm import Session
from db.db_crud.user_crud import UserCRUD
from main_files.setup import Setup
from services.auth_manager import AuthManager
from services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm


class UserService:
    @staticmethod
    def create_new_user(name: str, password: str, db: Session) -> dict:
        setup = Setup.initial_default_set_up()
        board_setup = Setup.return_set_up_board(setup, 1)
        user = UserCRUD.create_user(db, name, password, setup, True)
        token = AuthService.authenticate_user(db, OAuth2PasswordRequestForm(username=name, password=password))
        return {"user_name": user.name,
                "user_rating": user.rating,
                "board_setup": board_setup,
                "token": token}

    @staticmethod
    def login(form_data: OAuth2PasswordRequestForm, db: Session) -> dict:
        token = AuthService.authenticate_user(db, form_data)
        user = UserCRUD.get_user_by_name(db, form_data.username)
        if user.is_active:
            return {"error": "user is already active"}
        UserCRUD.update_user_activity(db, user.name, True)
        board_setup = Setup.return_set_up_board(user.setup, 1)
        return {"user_name": user.name,
                "user_rating": user.rating,
                "board_setup": board_setup,
                "token": token}

    @staticmethod
    async def log_out(token: str, db: Session):
        user_id = await AuthManager.verify_token(token)
        user = UserCRUD.get_user(db, user_id)
        if not user:
            return {"error": "User not found"}
        UserCRUD.update_user_activity(db, user.name, False)
        return {"message": f"User {user.name} logged out successfully"}

