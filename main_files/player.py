from websocket import WebSocket


class Player:
    def __init__(self, player_id: int, websocket: WebSocket, pieces_set_up=None, player_name=None):
        self.player_id = player_id
        self.player_name = player_name
        self.websocket = websocket
        self.pieces_set_up = pieces_set_up
