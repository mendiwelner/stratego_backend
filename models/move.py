from models.cell import Cell
from pydantic import BaseModel


class Move(BaseModel):
    from_cell: Cell
    to_cell: Cell

    def __str__(self):
        return f"from {self.from_cell} to {self.to_cell}"

    def get_reverse_move(self, matrix_size: int = 10) -> 'Move':
        return Move(from_cell=self.from_cell.get_reverse_cell(matrix_size), to_cell=self.to_cell.get_reverse_cell(matrix_size))

    @staticmethod
    def create(from_cell: Cell, to_cell: Cell) -> 'Move':
        return Move(from_cell=from_cell, to_cell=to_cell)

    def get_reversed_direction_move(self) -> 'Move':
        return Move(from_cell=self.to_cell, to_cell=self.from_cell)
