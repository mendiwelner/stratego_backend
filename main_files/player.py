from typing import List
from websocket import WebSocket
from models.move import Move


class Player:
    def __init__(self, player_id: int, websocket: WebSocket, setup=None, player_name=None):
        self.player_id = player_id
        self.player_name = player_name
        self.websocket = websocket
        self.setup = setup
        self.moves: List[Move] = []

    def __str__(self):
        moves_str = ", ".join(str(move) for move in self.moves) if self.moves else "No moves"
        return f"🔹 Player {self.player_id}: {self.player_name or 'Unknown'}, Moves: {moves_str}"
