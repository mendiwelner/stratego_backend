from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_crud.user_crud import UserCRUD
from db.db_manager.db_session_manager import DBSessionManager
from fastapi.security import OAuth2PasswordRequestForm
from services.user_service import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.post("/create_new_user")
def create_new_user(name: str, password: str, db: Session = Depends(DBSessionManager.get_db)) -> dict:
    return UserService.create_new_user(name, password, db)


@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(DBSessionManager.get_db)) -> dict:
    return UserService.login(form_data, db)


@user_router.put("/log_out/{token}")
async def log_out(token: str, db: Session = Depends(DBSessionManager.get_db)) -> dict:
    print("Logging out user...")
    return await UserService.log_out(token, db)


@user_router.get("/read_user/{user_id}")
def read_user(user_id: int, db: Session = Depends(DBSessionManager.get_db)) -> dict | None:
    return UserCRUD.get_user(db, user_id)


@user_router.get("/get_users/{users}")
def get_users(db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.get_users(db)


@user_router.delete("/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(DBSessionManager.get_db)) -> dict:
    return UserCRUD.delete_user(db, user_id)


@user_router.delete("/delete_all_users")
def delete_all_users(db: Session = Depends(DBSessionManager.get_db)) -> dict:
    return UserCRUD.delete_all_users(db)


@user_router.get("/active_count/{count}")
def get_active_users_count(db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.get_active_users_count(db)
