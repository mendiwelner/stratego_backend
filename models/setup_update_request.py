from pydantic import BaseModel
from models.piece import Piece


class SetupUpdateRequest(BaseModel):
    board_setup: list[list[Piece | str]]
