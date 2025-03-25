from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_manager.db_session_manager import DBSessionManager
from services.set_up_service import SetUpService

setup_router = APIRouter(
    prefix="/setup",
    tags=["setup"]
)


@setup_router.get("/get_set_up/{token}")
def get_set_up(token: str, db: Session = Depends(DBSessionManager.get_db)) -> dict:
    return SetUpService.get_set_up(token, db)


