import random
from typing import List
from models.cell import Cell
from models.piece import Piece
import copy


class Board:
    def __init__(self, game):
        self.game = game
        self.board_matrix = [["o" for _ in range(10)] for _ in range(10)]
        self.player_1_pieces = []
        self.player_2_pieces = []
        self.forbidden_cells = [
            Cell(row=4, column=2), Cell(row=4, column=3),
            Cell(row=5, column=2), Cell(row=5, column=3),
            Cell(row=4, column=6), Cell(row=4, column=7),
            Cell(row=5, column=6), Cell(row=5, column=7)
        ]

    def initial_board(self):
        self.initial_pieces()
        player_1_set_up = self.game.players[0].pieces_set_up
        player_2_set_up = self.game.players[1].pieces_set_up

        if player_1_set_up:
            self.append_player_set_up(player_1_set_up, 0, 4)
        else:
            self.initial_random_player_pieces(1, 0, 4)

        if player_2_set_up:
            self.append_player_set_up(player_2_set_up, 6, 10)
        else:
            self.initial_random_player_pieces(2, 6, 10)

        for forbidden_cell in self.forbidden_cells:
            self.board_matrix[forbidden_cell.row][forbidden_cell.column] = "x"

    def initial_pieces(self):
        self.player_1_pieces = self.create_player_pieces(1)
        self.player_2_pieces = self.create_player_pieces(2)

    @staticmethod
    def create_player_pieces(player_number: int) -> List[Piece]:
        pieces = [Piece(number_of_player=player_number, value="f")]
        pieces += [Piece(number_of_player=player_number, value="b")] * 6
        pieces.append(Piece(number_of_player=player_number, value="1"))
        pieces += [Piece(number_of_player=player_number, value="2")] * 8
        pieces += [Piece(number_of_player=player_number, value="3")] * 5
        pieces += [Piece(number_of_player=player_number, value="4")] * 4
        pieces += [Piece(number_of_player=player_number, value="5")] * 4
        pieces += [Piece(number_of_player=player_number, value="6")] * 4
        pieces += [Piece(number_of_player=player_number, value="7")] * 3
        pieces += [Piece(number_of_player=player_number, value="8")] * 2
        pieces.append(Piece(number_of_player=player_number, value="9"))
        pieces.append(Piece(number_of_player=player_number, value="10"))
        return pieces

    def append_player_set_up(self, player_set_up, start_row, end_row):
        for row_index in range(start_row, end_row):
            self.board_matrix[row_index] = player_set_up[row_index - start_row]

    def initial_random_player_pieces(self, player_number, start_row, end_row):
        selected_pieces = random.sample(
            self.player_1_pieces if player_number == 1 else self.player_2_pieces, 40
        )
        for row_index in range(start_row, end_row):
            self.board_matrix[row_index] = selected_pieces[
                                           (row_index - start_row) * 10: (row_index - start_row + 1) * 10]

    def in_cell(self, cell: Cell):
        return self.board_matrix[cell.row][cell.column]

    def put_in_cell(self, cell: Cell, value: Piece | str):
        self.board_matrix[cell.row][cell.column] = value

    def print_board(self):
        for row in self.board_matrix:
            for column in row:
                print(str(column), end="  ")
            print()

    def rotate_board_matrix(self):
        return [row[::-1] for row in self.board_matrix[::-1]]

    def player_1_matrix(self):
        rotated_matrix = copy.deepcopy(self.rotate_board_matrix())
        for row in rotated_matrix:
            for cell in row:
                if isinstance(cell, Piece) and cell.number_of_player == 2:
                    cell.value = ""
        return rotated_matrix

    def player_2_matrix(self):
        matrix_copy = copy.deepcopy(self.board_matrix)
        for row in matrix_copy:
            for cell in row:
                if isinstance(cell, Piece) and cell.number_of_player == 1:
                    cell.value = ""
        return matrix_copy

    @staticmethod
    def convert_to_board_with_pieces(board_matrix: List[List[str]], player_number: int) -> List[List[Piece]]:
        new_board_matrix = []
        for row in range(10):
            new_row = []
            for cell in range(10):
                piece = Piece(number_of_player=player_number, value=board_matrix[row][cell])
                new_row.append(piece)
            new_board_matrix.append(new_row)
        return new_board_matrix

    @staticmethod
    def initial_default_set_up() -> str:
        board_set_up = [
            ["2", "2", "2", "2", "2", "2", "b", "b", "2", "2"],
            ["6", "6", "7", "7", "7", "9", "8", "8", "b", "1"],
            ["6", "6", "5", "5", "b", "0", "5", "5", "4", "4"],
            ["3", "3", "3", "b", "f", "b", "3", "3", "4", "4"]
        ]
        return Board.set_up_matrix_to_string(board_set_up)

    @staticmethod
    def set_up_matrix_to_string(matrix: List[List[str]]) -> str:
        return ''.join(''.join(row) for row in matrix)

    @staticmethod
    def set_up_string_to_matrix(set_up_string: str) -> List[List[str]]:
        return [list(set_up_string[i:i + 10]) for i in range(0, len(set_up_string), 10)]
