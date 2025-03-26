from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.db_crud.user_crud import UserCRUD
from main_files.board import Board
from main_files.setup import Setup
from models.setup_update_request import SetupUpdateRequest
from services.auth_manager import AuthManager


class SetUpService:
    @staticmethod
    async def update_setup(token: str, setup_data: SetupUpdateRequest, db: Session) -> dict:
        user_id = await AuthManager.verify_token(token)
        user = UserCRUD.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        setup = Setup.set_up_pieces_matrix_to_string(setup_data.board_setup)
        user.setup = setup
        print(setup)
        db.commit()
        db.refresh(user)
        return {"message": "Board setup updated successfully", "board_setup": user.setup}

    @staticmethod
    def get_setup():
        setup = Setup.initial_default_set_up()
        board_setup = Setup.return_set_up_board(setup, 1)
        return {"board_setup": board_setup}

