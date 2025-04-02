import warnings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.game_routes import games_router
from routes.user_routes import user_router
from routes.set_up_routes import setup_router
import uvicorn
from services.user_service import UserService

# הסתרת אזהרות דיפרקציה
warnings.simplefilter("ignore", category=DeprecationWarning)

app = FastAPI()

# הוספת middleware של CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# הוספת routers
app.include_router(user_router)
app.include_router(games_router)
app.include_router(setup_router)


@app.on_event("startup")
async def startup():
    UserService.deactivate_all_users()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
