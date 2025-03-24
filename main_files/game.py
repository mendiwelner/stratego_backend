from typing import List, Dict
from fastapi import WebSocket
import json
from starlette.websockets import WebSocketDisconnect
from main_files.piece_encoder import PieceEncoder
from models.cell import Cell
from models.move import Move
from main_files.moving import Moving
from main_files.player import Player
from main_files.board import Board
import asyncio


class Game:
    def __init__(self, game_id: int):
        self.game_id = game_id
        self.players: List[Player] = []
        self.moves: List[str] = []
        self.board = Board(self)
        self.turn = 1
        self.player_turn = 1
        self.moving = Moving(self)

    async def connect_player(self, player_websocket: WebSocket, player_name: str):
        if len(self.players) < 2:
            self.players.append(Player(len(self.players) + 1, player_websocket, player_name=player_name))
            await self.send_connect_massage_to_players()
            return len(self.players)
        return 0

    async def send_connect_massage_to_players(self):
        if len(self.players) == 1:
            await self.players[0].websocket.send_text(json.dumps({"type": "message", "message": "waiting for another "
                                                                                                "player..."}))

        else:
            for player in self.players:
                await player.websocket.send_text(json.dumps({"type": "message", "message": "game is ready!"}))
            self.initial_game()
            await self.send_board_to_players()

    async def remove_player(self, player_id: int):
        for player in self.players:
            if player.player_id == player_id:
                self.players.remove(player)
        await self.players[0].websocket.send_text(json.dumps({"type": "message", "message": "other player disconnected"}))

    async def disconnect_players(self):
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
            return await self.process_move(player_id, move)
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

    async def process_move(self, player_id: int, move: Move):
        if self.moving.legal_move(move, player_id):
            return await self.moving.do_move(move, player_id)
        else:
            return "not a legal move!"

    async def send_response_to_player(self, player_id: int, response: dict) -> None:
        await self.players[player_id-1].websocket.send_text(json.dumps(response))

    async def send_response_to_players(self, player_1_response: dict, player_2_response: dict) -> None:
        await self.send_response_to_player(1, player_1_response)
        await self.send_response_to_player(2, player_2_response)

    async def send_same_response_to_players(self, response: dict) -> None:
        for player in self.players:
            await player.websocket.send_text(json.dumps(response))

    def is_full(self):
        return len(self.players) == 2

    def initial_game(self):
        self.board.initial_board()

    async def send_board_to_players(self):
        player_1_data = {
            "type": "board",
            "number_of_player": 1,
            "board": self.board.player_1_matrix(),
            "players_data": {
                "your_name": self.players[0].player_name,
                "opponent_name": self.players[1].player_name,
            }
        }
        player_2_data = {
            "type": "board",
            "number_of_player": 2,
            "board": self.board.player_2_matrix(),
            "players_data": {
                "your_name": self.players[1].player_name,
                "opponent_name": self.players[0].player_name,
            }
        }
        tasks = [
            self.players[0].websocket.send_text(json.dumps(player_1_data, cls=PieceEncoder)),
            self.players[1].websocket.send_text(json.dumps(player_2_data, cls=PieceEncoder))
        ]
        await asyncio.gather(*tasks)

    def flip_turn(self):
        self.turn += 1
        if self.player_turn == 1:
            self.player_turn = 2
        else:
            self.player_turn = 1
