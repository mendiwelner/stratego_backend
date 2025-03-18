from game import Game
from models.move import Move
from models.piece import Piece
from player import Player

if __name__ == "__main__":
    player_1_set_up = [
        [Piece(1, "flag"), Piece(1, "bomb"), Piece(1, "bomb"), Piece(1, "bomb"), Piece(1, "bomb"), Piece(1, "bomb"),
         Piece(1, "bomb"), Piece(1, "spy"), Piece(1, "2"), Piece(1, "2")],
        [Piece(1, "2"), Piece(1, "2"), Piece(1, "2"), Piece(1, "2"), Piece(1, "2"), Piece(1, "2"), Piece(1, "2"),
         Piece(1, "2"), Piece(1, "3"), Piece(1, "3")],
        [Piece(1, "3"), Piece(1, "3"), Piece(1, "3"), Piece(1, "4"), Piece(1, "4"), Piece(1, "4"), Piece(1, "4"),
         Piece(1, "5"), Piece(1, "5"), Piece(1, "5")],
        [Piece(1, "5"), Piece(1, "6"), Piece(1, "6"), Piece(1, "6"), Piece(1, "6"), Piece(1, "7"), Piece(1, "7"),
         Piece(1, "7"), Piece(1, "8"), Piece(1, "8")]
    ]

    player_2_set_up = [
        [Piece(2, "flag"), Piece(2, "bomb"), Piece(2, "bomb"), Piece(2, "bomb"), Piece(2, "bomb"), Piece(2, "bomb"),
         Piece(2, "bomb"), Piece(2, "spy"), Piece(2, "2"), Piece(2, "2")],
        [Piece(2, "2"), Piece(2, "2"), Piece(2, "2"), Piece(2, "2"), Piece(2, "2"), Piece(2, "2"), Piece(2, "2"),
         Piece(2, "2"), Piece(2, "3"), Piece(2, "3")],
        [Piece(2, "3"), Piece(2, "3"), Piece(2, "3"), Piece(2, "4"), Piece(2, "4"), Piece(2, "4"), Piece(2, "4"),
         Piece(2, "5"), Piece(2, "5"), Piece(2, "5")],
        [Piece(2, "5"), Piece(2, "6"), Piece(2, "6"), Piece(2, "6"), Piece(2, "6"), Piece(2, "7"), Piece(2, "7"),
         Piece(2, "7"), Piece(2, "8"), Piece(2, "8")]
    ]

    player1 = Player(1, None, player_1_set_up)
    player2 = Player(2, None, player_2_set_up)
    game = Game(1)
    game.players = [player1, player2]
    game.initial_game()
    game.board.print_board()
    move = {"from_cell": {"row": 6, "column": 8}, "to_cell": {"row": 5, "column": 8}}
    move = Move(**move)
    try:
        print(game.moving.is_legal_move(move, 2))
    except Exception as e:
        print(e)
    game.moving.do_move(move)
    game.board.print_board()
