import os
from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
from services.game_manage import GameManage
from pyngrok import ngrok
import uvicorn

app = FastAPI()

# הוספת middleware של CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_all_games")
async def get_all_games():
    return GameManage.return_all_games()


@app.get("/get_game")
async def get_game(game_number: int):
    return GameManage.return_game(game_number)


@app.post("/create_game")
async def create_game():
    return GameManage.create_game()


@app.websocket("/player_connect_game")
async def player_connect_game(player_websocket: WebSocket):
    await GameManage.player_connect_game(player_websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
