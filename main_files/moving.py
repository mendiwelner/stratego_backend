from typing import List
from models.cell import Cell
from models.move import Move
from models.move_to_client import MoveToClient
from models.piece import Piece


class Moving:
    def __init__(self, game):
        self.game = game
        self.board = game.board

    def legal_move(self, move, player_id) -> bool:
        # todo
        return True
        # try:
        #     return self.is_legal_move(move, player_id)
        # except Exception:
        #     return False

    def is_legal_move(self, move: Move, player_id: int) -> bool:
        in_from_cell = self.board.in_cell(move.from_cell)
        in_to_cell = self.board.in_cell(move.to_cell)
        if not isinstance(in_from_cell, Piece):
            raise Exception("not piece in from cell")
        elif in_from_cell.number_of_player != player_id:
            raise Exception("other player piece in from cell")
        elif in_from_cell.value == "b":
            raise Exception("bomb in from cell, can't move")
        elif in_from_cell.value == "f":
            raise Exception("flag in from cell, can't move")
        elif isinstance(in_to_cell, Piece) and in_to_cell.number_of_player == player_id:
            raise Exception("can't move there, it's your piece there")
        elif in_to_cell == "x":
            raise Exception("can't move there, it's a lake there")
        elif in_from_cell.value != "2":
            return self.check_none_2_piece_move(move)
        elif in_from_cell.value == "2":
            return self.check_2_piece_move(move)

    async def do_move(self, move: Move, player_id: int) -> None:
        if player_id == 1:
            move = move.get_reverse_move()
        move_to_client = await self.do_move_in_board(move)
        await self.game.send_response_to_players({
            "type": "make_move",
            "move": move_to_client.get_move_to_client(1).model_dump()
        },
            {
                "type": "make_move",
                "move": move_to_client.get_move_to_client(2).model_dump()
            },
        )
        self.game.flip_turn()

    async def do_move_in_board(self, move: Move) -> MoveToClient:
        in_from_cell = self.board.in_cell(move.from_cell)
        in_to_cell = self.board.in_cell(move.to_cell)
        if isinstance(in_to_cell, Piece):
            return await self.attack_move(move, in_from_cell, in_to_cell)
        else:
            self.board.put_in_cell(move.from_cell, "o")
            self.board.put_in_cell(move.to_cell, in_from_cell)
            return MoveToClient(move_type="move", from_cell=move.from_cell, to_cell=move.to_cell,
                                in_from_cell="o", in_to_cell=in_from_cell,
                                in_from_cell_show=None, in_to_cell_show=None)

    async def attack_move(self, move: Move, in_from_cell: Piece, in_to_cell: Piece) -> MoveToClient:
        loser = in_from_cell.return_losers_in_attack(in_to_cell)
        self.board.put_in_cell(move.from_cell, "o")
        attacker_position = self.calculate_attacker_position(move, in_from_cell)
        if loser == 0:
            self.board.put_in_cell(move.to_cell, "o")
            await self.send_to_graveyard(0, in_from_cell, in_to_cell)
            return MoveToClient(move_type="attack", from_cell=move.from_cell, to_cell=move.to_cell,
                                in_from_cell="o", in_to_cell="o",
                                in_from_cell_show=in_from_cell, in_to_cell_show=in_to_cell,
                                attacker_position=attacker_position)
        elif loser == 1:
            await self.send_to_graveyard(1, in_from_cell, in_to_cell)
            return MoveToClient(move_type="attack", from_cell=move.from_cell, to_cell=move.to_cell,
                                in_from_cell="o", in_to_cell=in_to_cell,
                                in_from_cell_show=in_from_cell, in_to_cell_show=in_to_cell,
                                attacker_position=attacker_position)
        elif loser == 2:
            await self.send_to_graveyard(2, in_from_cell, in_to_cell)
            self.board.put_in_cell(move.to_cell, in_from_cell)
            return MoveToClient(move_type="attack", from_cell=move.from_cell, to_cell=move.to_cell,
                                in_from_cell="o", in_to_cell=in_from_cell,
                                in_from_cell_show=in_from_cell, in_to_cell_show=in_to_cell,
                                attacker_position=attacker_position)

    @staticmethod
    def calculate_attacker_position(move: Move, in_from_cell: Piece) -> Cell | None:
        attacker_position = None
        if in_from_cell.value == "2":
            if abs(move.from_cell.row - move.to_cell.row) > 1 or abs(move.from_cell.column - move.to_cell.column) > 1:
                row_direction = 1 if move.to_cell.row > move.from_cell.row else -1 \
                    if move.to_cell.row < move.from_cell.row else 0
                col_direction = 1 if move.to_cell.column > move.from_cell.column else -1 \
                    if move.to_cell.column < move.from_cell.column else 0
                attacker_position = Cell(row=move.to_cell.row - row_direction,
                                         column=move.to_cell.column - col_direction)
        return attacker_position

    @staticmethod
    def check_none_2_piece_move(move: Move) -> bool:
        row_diff = abs(move.to_cell.row - move.from_cell.row)
        col_diff = abs(move.to_cell.column - move.from_cell.column)
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

    def check_2_piece_move(self, move: Move) -> bool:
        from_row, from_col = move.from_cell.row, move.from_cell.column
        to_row, to_col = move.to_cell.row, move.to_cell.column
        if from_row != to_row and from_col != to_col:
            raise Exception("can't move there")
        row_step = 1 if to_row > from_row else -1 if to_row < from_row else 0
        col_step = 1 if to_col > from_col else -1 if to_col < from_col else 0
        current_row, current_col = from_row + row_step, from_col + col_step
        while (current_row, current_col) != (to_row, to_col):
            if self.board.in_cell(Cell(row=current_row, column=current_col)) != "o":
                raise Exception("way is not clear")
            current_row += row_step
            current_col += col_step
        return True

    def can_move(self, player_id: int, cell: Cell) -> dict:
        if player_id == 1:
            cell = cell.get_reverse_cell()
        cell_content = self.board.in_cell(cell)
        error = self.check_errors_in_move(player_id, cell_content)
        if error is not None:
            return error
        if cell_content.value == "2":
            can_move_to = self.piece_2_can_move_to(cell, player_id)
        else:
            can_move_to = [
                neighbor_cell for neighbor_cell in cell.return_neighbors()
                if self.can_move_there(neighbor_cell, player_id)
            ]
        if not can_move_to:
            return {"type": "error_cell_pushed", "message": "Cell can't move anywhere!"}
        if player_id == 1:
            cell = cell.get_reverse_cell()
            can_move_to = [c.get_reverse_cell() for c in can_move_to]
        return {
            "type": "mark_cell",
            "cell": {"row": cell.row, "column": cell.column},
            "possible_moves": [{"row": c.row, "column": c.column} for c in can_move_to]
        }

    def piece_2_can_move_to(self, cell: Cell, player_id: int) -> List[Cell]:
        can_move_to = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for row_step, col_step in directions:
            current_row, current_col = cell.row + row_step, cell.column + col_step
            while 0 <= current_row < 10 and 0 <= current_col < 10:
                next_cell = Cell(row=current_row, column=current_col)
                if not self.can_move_there(next_cell, player_id):
                    break
                can_move_to.append(next_cell)
                if isinstance(self.board.in_cell(next_cell), Piece):
                    break
                current_row += row_step
                current_col += col_step
        return can_move_to

    def can_move_there(self, cell: Cell, player_id: int) -> bool:
        in_cell = self.board.in_cell(cell)
        if in_cell == 'x':
            return False
        elif in_cell == 'o':
            return True
        elif in_cell.number_of_player == player_id:
            return False
        elif in_cell.number_of_player != player_id:
            return True

    def check_errors_in_move(self, player_id: int, cell_content: Piece) -> dict | None:
        if self.game.player_turn != player_id:
            return {"type": "error_cell_pushed", "message": "It's not your turn"}
        if cell_content in ['o', 'x']:
            return {"type": "error_cell_pushed", "message": "Not a piece there"}
        elif cell_content.number_of_player != player_id:
            return {"type": "error_cell_pushed", "message": "Not your piece there"}
        elif cell_content.value == "b" or cell_content.value == "f":
            return {"type": "error_cell_pushed", "message": "This piece can't move!"}
        return None

    async def send_to_graveyard(self, number_of_loser: int, in_from_cell: Piece, in_to_cell: Piece) -> None:
        if number_of_loser == 0:
            await self.game.send_same_response_to_players({"type": "piece_captured", "piece": in_from_cell.to_dict()})
            await self.game.send_same_response_to_players({"type": "piece_captured", "piece": in_to_cell.to_dict()})
        elif number_of_loser == 1:
            await self.game.send_same_response_to_players({"type": "piece_captured", "piece": in_from_cell.to_dict()})
        elif number_of_loser == 2:
            await self.game.send_same_response_to_players({"type": "piece_captured", "piece": in_to_cell.to_dict()})
