from db.db_crud.user_crud import UserCRUD
from main_files.game import Game
from fastapi import WebSocket, WebSocketDisconnect
from db.db_manager.db_session_manager import DBSessionManager
from sqlalchemy.orm import Session
from services.auth_manager import AuthManager


class GameManage:
    games = {}

    @staticmethod
    def create_game() -> int:
        game_id = len(GameManage.games) + 1
        GameManage.games[game_id] = Game(game_id)
        return game_id

    @staticmethod
    def find_available_game_or_create() -> Game:
        for game in GameManage.games.values():
            if not game.is_full():
                return game
        game_id = GameManage.create_game()
        return GameManage.games[game_id]

    @staticmethod
    async def find_game_and_accept_player(player_websocket: WebSocket) -> (Game, int):
        available_game = GameManage.find_available_game_or_create()
        game_id = available_game.game_id
        await player_websocket.accept()
        return available_game, game_id

    @staticmethod
    async def player_connect_game(player_websocket: WebSocket) -> None:
        game, game_id = await GameManage.find_game_and_accept_player(player_websocket)
        token = AuthManager.extract_token_from_websocket(player_websocket)
        if not await AuthManager.verify_token_and_close_websocket(player_websocket, token):
            return
        user_id = await AuthManager.verify_token(token)
        player_name, setup, rating = GameManage.get_details_from_user_id(user_id)
        player_id = await game.connect_player(player_websocket, player_name, setup, rating)
        await GameManage.process_player_to_game_connection(player_websocket, player_id, game)

    @staticmethod
    def get_details_from_user_id(user_id: int,  db: Session = DBSessionManager.get_db()) -> (str, str, int):
        return (UserCRUD.get_user(db=db, user_id=user_id).name,
                UserCRUD.get_user(db=db, user_id=user_id).setup,
                UserCRUD.get_user(db=db, user_id=user_id).rating)

    @staticmethod
    async def process_player_to_game_connection(player_websocket: WebSocket, player_id: int, game: Game) -> None:
        try:
            await GameManage.get_data_and_send_response(player_websocket, player_id, game)
        except WebSocketDisconnect:
            await game.player_leaving_the_game(player_id)
            await GameManage.delete_game(game.game_id)
        except Exception as exception:
            await GameManage.handle_exception(exception, player_websocket)

    @staticmethod
    async def handle_exception(exception: Exception, player_websocket: WebSocket) -> None:
        reason = f"⚠️ Unexpected error: {exception}"
        print(reason)
        await player_websocket.close(code=1011, reason=reason)

    @staticmethod
    async def get_data_and_send_response(player_websocket: WebSocket, player_id: int, game) -> None:
        while True:
            data = await player_websocket.receive_json()
            response = await game.process_data(player_id, data)
            await game.game_messenger.send_response_to_player(player_id, response)

    @classmethod
    def return_all_games(cls) -> dict:
        return cls.games

    @classmethod
    def return_game(cls, game_number) -> Game:
        return cls.games.get(game_number, None)

    @classmethod
    async def delete_game(cls, game_id: int) -> None:
        game = cls.games.get(game_id)
        if game:
            await game.disconnect_players()
            del cls.games[game_id]
