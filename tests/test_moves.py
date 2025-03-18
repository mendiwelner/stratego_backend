import pytest
from unittest.mock import MagicMock
from game import Game
from models.move import Move
from models.cell import Cell
from models.piece import Piece


@pytest.fixture
def game():
    game_instance = Game(game_id=1)
    game_instance.board = MagicMock()  # Mock the board
    return game_instance


def test_legal_move_valid_move(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=1))
    game.board.in_cell.side_effect = [Piece(number_of_player=1, value="3"),
                                      "o"]  # Mock piece in from cell, empty destination

    assert game.moving.legal_move(move, 1) is True


def test_legal_move_no_piece_in_from_cell(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=1))
    game.board.in_cell.side_effect = ["o", "o"]  # No piece in from cell

    assert game.moving.legal_move(move, 1) is False


def test_legal_move_other_player_piece(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=1))
    game.board.in_cell.side_effect = [Piece(number_of_player=2, value="3"), "o"]  # Other player's piece in from cell

    assert game.moving.legal_move(move, 1) is False


def test_legal_move_bomb_piece(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=1))
    game.board.in_cell.side_effect = [Piece(number_of_player=1, value="bomb"), "o"]  # Bomb piece in from cell

    assert game.moving.legal_move(move, 1) is False


def test_legal_move_flag_piece(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=1))
    game.board.in_cell.side_effect = [Piece(number_of_player=1, value="flag"), "o"]  # Flag piece in from cell

    assert game.moving.legal_move(move, 1) is False


def test_legal_move_friendly_piece_in_target(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=1))
    game.board.in_cell.side_effect = [Piece(number_of_player=1, value="3"),
                                      Piece(number_of_player=1, value="4")]  # Own piece in destination

    assert game.moving.legal_move(move, 1) is False


def test_legal_move_lake_target(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=1))
    game.board.in_cell.side_effect = [Piece(number_of_player=1, value="3"), "x"]  # Lake in target cell

    assert game.moving.legal_move(move, 1) is False


def test_legal_move_scout_moves_straight_path(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=5))
    game.board.in_cell.side_effect = [Piece(number_of_player=1, value="2"), "o", "o", "o", "o",
                                      "o"]  # Scout moves in straight path

    assert game.moving.legal_move(move, 1) is True


def test_legal_move_scout_blocked_path(game):
    move = Move(from_cell=Cell(row=0, column=0), to_cell=Cell(row=0, column=5))
    game.board.in_cell.side_effect = [Piece(number_of_player=1, value="2"), "o", "o",
                                      Piece(number_of_player=2, value="4"), "o", "o"]  # Scout is blocked

    assert game.moving.legal_move(move, 1) is False
