from game import Game
from fastapi import WebSocket, WebSocketDisconnect


class GameManage:
    games = {}

    @staticmethod
    def create_game():
        game_id = len(GameManage.games) + 1
        GameManage.games[game_id] = Game(game_id)
        return game_id

    @staticmethod
    def find_available_game_or_create():
        for game in GameManage.games.values():
            if not game.is_full():
                return game
        game_id = GameManage.create_game()
        return GameManage.games[game_id]

    @staticmethod
    async def player_connect_game(player_websocket: WebSocket):
        available_game = GameManage.find_available_game_or_create()
        game_id = available_game.game_id
        await player_websocket.accept()
        player_id = await available_game.connect_player(player_websocket)
        try:
            while True:
                data = await player_websocket.receive_json()
                response = await available_game.process_data(player_id, data)
                await available_game.send_response_to_player(player_id, response)
        except WebSocketDisconnect:
            await GameManage.delete_game(game_id)
        except Exception as e:
            reason = f"⚠️ Unexpected error: {e}"
            print(reason)
            await player_websocket.close(code=1011, reason=reason)

    @classmethod
    def return_all_games(cls):
        return cls.games

    @classmethod
    def return_game(cls, game_number):
        return cls.games.get(game_number, None)

    @classmethod
    async def delete_game(cls, game_id: int):
        game = cls.games.get(game_id)
        if game:
            await game.disconnect_players()
            del cls.games[game_id]


