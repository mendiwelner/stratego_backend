from sqlalchemy.orm import Session
from db.db_crud.user_crud import UserCRUD
from main_files.board import Board
from services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm


class UserService:
    @staticmethod
    def create_new_user(name: str, password: str, db: Session) -> dict:
        setup = Board.initial_default_set_up()
        board_setup = Board.return_set_up_board(setup, 1)
        UserCRUD.create_user(db, name, password, setup)
        token = AuthService.authenticate_user(db, OAuth2PasswordRequestForm(username=name, password=password))
        return {"user_name": name, "board_setup": board_setup, "token": token}

    @staticmethod
    def login(form_data: OAuth2PasswordRequestForm, db: Session) -> dict:
        token = AuthService.authenticate_user(db, form_data)
        user = UserCRUD.get_user_by_name(db, form_data.username)
        board_setup = Board.return_set_up_board(user.setup, 1)
        return {"user_name": user.name, "board_setup": board_setup, "token": token}

