from websocket import WebSocket


class Player:
    def __init__(self, player_id: int, websocket: WebSocket, pieces_set_up=None):
        self.player_id = player_id
        self.websocket = websocket
        self.pieces_set_up = pieces_set_up
