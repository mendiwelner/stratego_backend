from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.game_routes import games_router
from routes.user_routes import router as user_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(games_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
