from typing import List, Dict
from fastapi import WebSocket
import json
from starlette.websockets import WebSocketDisconnect
from main_files.game_messenger import GameMessenger
from models.cell import Cell
from models.move import Move
from main_files.moving import Moving
from main_files.player import Player
from main_files.board import Board


class Game:
    def __init__(self, game_id: int):
        self.game_id = game_id
        self.players: List[Player] = []
        self.moves: List[str] = []
        self.board = Board(self)
        self.turn = 1
        self.player_turn = 1
        self.moving = Moving(self)
        self.game_messenger = GameMessenger(self)

    async def connect_player(self, player_websocket: WebSocket, player_name: str, setup: str) -> int:
        if len(self.players) < 2:
            self.players.append(Player(player_id=len(self.players) + 1,
                                       websocket=player_websocket,
                                       setup=setup,
                                       player_name=player_name))
            await self.game_messenger.send_connect_massage_to_players()
            return len(self.players)
        return 0

    async def remove_player(self, player_id: int) -> None:
        for player in self.players:
            if player.player_id == player_id:
                self.players.remove(player)
        await self.players[0].websocket.send_text(json.dumps({"type": "message", "message": "other player disconnected"}))

    async def disconnect_players(self) -> None:
        for player in self.players[:]:
            try:
                await player.websocket.send_text(
                    json.dumps({"type": "message", "message": "game closed!"})
                )
            except WebSocketDisconnect:
                pass
            except Exception as e:
                print(f"Error when trying to send a message to the player: {e}")
            try:
                await player.websocket.close()
            except Exception as e:
                print(f"Error when trying to close the player's connection: {e}")
            self.players.remove(player)

    async def process_data(self, player_id: int, data: Dict) -> dict:
        if data["action"] == "make_move":
            move = Move(**data["move"])
            move_state = await self.process_move(player_id, move)
            return {"type": "message", "message": move_state}
        elif data["action"] == "check_cell_move":
            cell = Cell(**data["cell"])
            return self.moving.can_move(player_id, cell)
        elif data["action"] == "check_cell_hover":
            cell = Cell(**data["cell"])
            return self.convert_mark_to_hover_data(cell, player_id)

    def convert_mark_to_hover_data(self, cell: Cell, player_id: int) -> dict:
        data = self.moving.can_move(player_id, cell)
        if data["type"] == "error_cell_pushed":
            data["type"] = "error_cell_hovered"
        elif data["type"] == "mark_cell":
            data["type"] = "mark_cell_hover"
        return data

    async def process_move(self, player_id: int, move: Move) -> str:
        if self.moving.legal_move(move, player_id):
            await self.moving.do_move(move, player_id)
            return "move done!"
        else:
            return "not a legal move!"

    def is_full(self) -> bool:
        return len(self.players) == 2

    def initial_game(self) -> None:
        self.board.initial_board()

    def flip_turn(self) -> None:
        self.turn += 1
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1
