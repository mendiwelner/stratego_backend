from websocket import WebSocket


class Player:
    def __init__(self, player_id: int, websocket: WebSocket, setup=None, player_name=None):
        self.player_id = player_id
        self.player_name = player_name
        self.websocket = websocket
        self.setup = setup
