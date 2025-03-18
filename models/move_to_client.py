from pydantic import BaseModel
from models.cell import Cell
from models.piece import Piece


class MoveToClient(BaseModel):
    move_type: str
    from_cell: Cell
    to_cell: Cell
    in_from_cell: Piece | str
    in_to_cell: Piece | str
    in_from_cell_show: Piece | str | None
    in_to_cell_show: Piece | str | None
    attacker_position: Cell | None = None

    def get_move_to_client(self, player_id: int, matrix_size: int = 10) -> 'MoveToClient':
        from_cell, to_cell, attacker_position = (
            self.from_cell.get_reverse_cell(matrix_size),
            self.to_cell.get_reverse_cell(matrix_size),
            self.attacker_position.get_reverse_cell(matrix_size) if self.attacker_position else None
        ) if player_id == 1 else (
            self.from_cell, self.to_cell, self.attacker_position
        )

        in_to_cell = self.in_to_cell
        if isinstance(self.in_to_cell, Piece) and self.in_to_cell.number_of_player != player_id:
            in_to_cell = Piece(number_of_player=self.in_to_cell.number_of_player, value="")

        return MoveToClient(
            move_type=self.move_type,
            from_cell=from_cell,
            to_cell=to_cell,
            in_from_cell=self.in_from_cell,
            in_to_cell=in_to_cell,
            in_from_cell_show=self.in_from_cell_show,
            in_to_cell_show=self.in_to_cell_show,
            attacker_position=attacker_position
        )

