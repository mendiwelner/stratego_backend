import random
from typing import List
from main_files.setups import Setups
from models.piece import Piece


class Setup:
    @staticmethod
    def initial_default_set_up() -> str:
        board_set_up = random.choice(Setups.board_setups)
        return Setup.set_up_matrix_to_string(board_set_up)

    @staticmethod
    def set_up_matrix_to_string(matrix: List[List[str]]) -> str:
        return ''.join(''.join(row) for row in matrix)

    @staticmethod
    def set_up_pieces_matrix_to_string(matrix: List[List[Piece]]) -> str:
        return ''.join(
            ''.join('0' if piece.value == '10' else str(piece.value) for piece in row if isinstance(piece, Piece))
            for row in matrix
        )

    @staticmethod
    def set_up_string_to_matrix(set_up_string: str) -> List[List[str]]:
        return [list(set_up_string[i:i + 10]) for i in range(0, len(set_up_string), 10)]

    @staticmethod
    def return_set_up_board(setup: str, player_number: int) -> List[List[Piece]]:
        set_up_matrix = Setup.set_up_string_to_matrix(setup)
        piece_matrix = Setup.string_matrix_to_board(set_up_matrix, player_number)
        empty_matrix = [["" for column in range(10)] for row in range(6)]
        return empty_matrix + piece_matrix

    @staticmethod
    def string_matrix_to_board(matrix: List[List[str]], player_number: int):
        return [[Piece(number_of_player=player_number, value=str(10) if value == '0' else str(value))
                 for value in row] for row in matrix]

    @staticmethod
    def reverse_set_up_matrix(matrix: List[List[str]]) -> List[List[str]]:
        return [[matrix[3 - row][9 - col] for col in range(10)] for row in range(4)]
