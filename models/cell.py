from typing import List
from pydantic import BaseModel


class Cell(BaseModel):
    row: int
    column: int

    def __str__(self):
        return f"Cell(row={self.row}, column={self.column})"

    def return_neighbors(self, matrix_size: int = 10) -> List['Cell']:
        neighbors = []
        possible_neighbors = [
            (-1, 0),  # מעל
            (1, 0),   # מתחת
            (0, -1),  # שמאלה
            (0, 1)    # ימינה
        ]
        for dr, dc in possible_neighbors:
            new_row, new_col = self.row + dr, self.column + dc
            if 0 <= new_row < matrix_size and 0 <= new_col < matrix_size:
                neighbors.append(Cell(row=new_row, column=new_col))
        return neighbors

    def get_reverse_cell(self, matrix_size: int = 10) -> 'Cell':
        reverse_row = matrix_size - 1 - self.row
        reverse_column = matrix_size - 1 - self.column
        return Cell(row=reverse_row, column=reverse_column)
