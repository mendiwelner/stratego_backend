from typing import List, Dict
from fastapi import WebSocket
import json
from main_files.game_messenger import GameMessenger
from main_files.rating import Rating
from models.cell import Cell
from models.move import Move
from main_files.moving import Moving
from main_files.player import Player
from main_files.board import Board
from fastapi import WebSocketDisconnect
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
        self.game_messenger = GameMessenger(self)

    async def connect_player(self, player_websocket: WebSocket, player_name: str, setup: str, rating: int) -> int:
        if len(self.players) < 2:
            self.players.append(Player(player_id=len(self.players) + 1,
                                       websocket=player_websocket,
                                       setup=setup,
                                       player_name=player_name,
                                       rating=rating))
            await self.game_messenger.send_connect_massage_to_players()
            return len(self.players)
        return 0

    async def remove_player(self, player_id: int) -> None:
        for player in self.players:
            if player.player_id == player_id:
                self.players.remove(player)
        message = {"type": "message", "message": "other player disconnected"}
        await self.players[0].websocket.send_text(json.dumps(message))

    async def disconnect_players(self) -> None:
        for player in self.players[:]:
            try:
                await player.websocket.send_text(
                    json.dumps({"type": "message", "message": "game closed!"})
                )
            except WebSocketDisconnect:
                pass
            except (WebSocketDisconnect, RuntimeError):
                pass
            try:
                await player.websocket.close()
            except (WebSocketDisconnect, RuntimeError):
                pass
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
        elif data["action"] == "disconnect":
            return await self.player_leaving_the_game(player_id)

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
            await self.check_win_and_send_messages()
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

    async def check_win_and_send_messages(self) -> None:
        player_1_rating = self.players[0].rating
        player_2_rating = self.players[1].rating
        loser = self.board.check_loser_by_flag()
        reason = "flag_occupied"
        if loser == 0:
            loser = self.board.check_loser_by_moved_pieces()
            reason = "no_moved_pieces"
        if loser != 0:
            Rating.update_players_rating(self.players, loser)
            player_1_rating_change = self.players[0].rating - player_1_rating
            player_2_rating_change = self.players[1].rating - player_2_rating
            messages = {
                1: {
                    "player_1_result": "loser",
                    "player_2_result": "winner",
                },
                2: {
                    "player_1_result": "winner",
                    "player_2_result": "loser",
                },
                3: {
                    "player_1_result": "draw",
                    "player_2_result": "draw",
                    "reason": "no_moved_pieces"
                }
            }
            player_1_data = {
                "type": "endgame",
                "result": messages[loser].get("player_1_result", "draw"),
                "reason": reason,
                "rating_change": player_1_rating_change
            }
            player_2_data = {
                "type": "endgame",
                "result": messages[loser].get("player_2_result", "draw"),
                "reason": reason,
                "rating_change": player_2_rating_change
            }
            await asyncio.sleep(1.4)
            await self.game_messenger.send_response_to_players(player_1_data, player_2_data)

    async def player_leaving_the_game(self, player_id: int) -> dict:
        if player_id == 1:
            loser_index, winner_index = 0, 1
        else:
            loser_index, winner_index = 1, 0
        player_loser = self.players[loser_index]
        player_winner = self.players[winner_index]
        initial_loser_rating = player_loser.rating
        initial_winner_rating = player_winner.rating
        Rating.update_players_rating(self.players, player_loser.player_id)
        loser_rating_change = player_loser.rating - initial_loser_rating
        winner_rating_change = player_winner.rating - initial_winner_rating
        winner_data = {
            "type": "endgame",
            "result": "winner",
            "reason": "leaving",
            "rating_change": winner_rating_change
        }
        loser_data = {
            "type": "endgame",
            "result": "loser",
            "reason": "leaving",
            "rating_change": loser_rating_change
        }
        if player_winner.player_id < player_loser.player_id:
            await self.game_messenger.send_response_to_players(winner_data, loser_data)
        else:
            await self.game_messenger.send_response_to_players(loser_data, winner_data)
        return {"type": "message", "message": f"player {player_id} left the game"}


