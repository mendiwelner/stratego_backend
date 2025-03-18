from models.cell import Cell
from pydantic import BaseModel


class Move(BaseModel):
    from_cell: Cell
    to_cell: Cell

    def __str__(self):
        return f"from {self.from_cell} to {self.to_cell}"

    def get_reverse_move(self, matrix_size: int = 10) -> 'Move':
        return Move(from_cell=self.from_cell.get_reverse_cell(matrix_size), to_cell=self.to_cell.get_reverse_cell(matrix_size))
