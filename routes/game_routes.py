from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.orm import Session
from db.db_crud.game_crud import GameCRUD
from db.db_manager.db_session_manager import DBSessionManager
from services.game_manage import GameManage


games_router = APIRouter(
    prefix="/games",
    tags=["games"]
)


@games_router.get("/get_all_games")
async def get_all_games():
    return GameManage.return_all_games()


@games_router.get("/get_game/{user_id}")
async def get_game(game_number: int):
    return GameManage.return_game(game_number)


@games_router.post("/create_game")
async def create_game():
    return GameManage.create_game()


@games_router.post("/add_game/{game_name}")
async def add_game(game_name: str, db: Session = Depends(DBSessionManager.get_db)):
    return GameCRUD.create_game(db, game_name)


@games_router.get("/gat_games_data")
def gat_games_data(db: Session = Depends(DBSessionManager.get_db)):
    return GameCRUD.get_games(db)


@games_router.websocket("/player_connect_game")
async def player_connect_game(player_websocket: WebSocket):
    await GameManage.player_connect_game(player_websocket)

