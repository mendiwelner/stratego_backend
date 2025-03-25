from sqlalchemy.orm import Session

from db.db_crud.user_crud import UserCRUD
from main_files.board import Board
from services.auth_manager import AuthManager


class SetUpService:
    @staticmethod
    def get_set_up(token: str, db: Session) -> dict:
        user_id = AuthManager.verify_token(token)
        setup = UserCRUD.get_user(db, user_id).setup
        board_setup = Board.return_set_up_board(setup, 1)
        return {"board_setup": board_setup}
