from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.game_routes import games_router
from routes.user_routes import router as user_router
import uvicorn
from pyngrok import ngrok

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


def start_ngrok():
    url = ngrok.connect(8000)
    print(f"FastAPI is publicly accessible at: {url}")
    return url


if __name__ == "__main__":
    public_url = start_ngrok()
    uvicorn.run(app, host="0.0.0.0", port=8000)
