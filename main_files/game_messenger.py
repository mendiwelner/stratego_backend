from main_files.piece_encoder import PieceEncoder
import json
import asyncio
from fastapi.websockets import WebSocketState


class GameMessenger:
    def __init__(self, game):
        self.game = game

    async def send_connect_massage_to_players(self) -> None:
        if len(self.game.players) == 1:
            await self.game.players[0].websocket.send_text(json.dumps({"type": "message", "message": "waiting for another "
                                                                                                "player..."}))
        else:
            for player in self.game.players:
                await player.websocket.send_text(json.dumps({"type": "message", "message": "game is ready!"}))
            self.game.initial_game()
            await self.send_board_to_players()

    async def send_board_to_players(self) -> None:
        self.game.board.initial_test_board()
        player_1_data = {
            "type": "board",
            "number_of_player": 1,
            "board": self.game.board.player_1_matrix(),
            "players_data": {
                "your_name": self.game.players[0].player_name,
                "opponent_name": self.game.players[1].player_name,
            }
        }
        player_2_data = {
            "type": "board",
            "number_of_player": 2,
            "board": self.game.board.player_2_matrix(),
            "players_data": {
                "your_name": self.game.players[1].player_name,
                "opponent_name": self.game.players[0].player_name,
            }
        }
        tasks = [
            self.game.players[0].websocket.send_text(json.dumps(player_1_data, cls=PieceEncoder)),
            self.game.players[1].websocket.send_text(json.dumps(player_2_data, cls=PieceEncoder))
        ]
        await asyncio.gather(*tasks)

    async def send_response_to_players(self, player_1_response: dict, player_2_response: dict) -> None:
        await self.send_response_to_player(1, player_1_response)
        await self.send_response_to_player(2, player_2_response)

    async def send_same_response_to_players(self, response: dict) -> None:
        for player in self.game.players:
            if player.websocket.client_state == WebSocketState.CONNECTED:
                await player.websocket.send_text(json.dumps(response))

    async def send_response_to_player(self, player_id: int, response: dict) -> None:
        await self.game.players[player_id - 1].websocket.send_text(json.dumps(response))
