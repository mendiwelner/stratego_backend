from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_manager.db_session_manager import DBSessionManager
from models.setup_update_request import SetupUpdateRequest
from services.set_up_service import SetUpService

setup_router = APIRouter(
    prefix="/setup",
    tags=["setup"]
)


@setup_router.put("/update_setup/{token}")
async def update_setup(token: str, setup_data: SetupUpdateRequest, db: Session = Depends(DBSessionManager.get_db)) -> dict:
    return await SetUpService.update_setup(token, setup_data, db)


@setup_router.put("/get_setup/")
def get_setup() -> dict:
    return SetUpService.get_setup()


