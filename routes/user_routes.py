from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_crud.user_crud import UserCRUD
from db.db_manager.db_session_manager import DBSessionManager
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_service import AuthService
from services.user_service import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@user_router.post("/")
def create_new_user(name: str, password: str, db: Session = Depends(DBSessionManager.get_db)) -> dict:
    return UserService.create_new_user(name, password, db)


@user_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(DBSessionManager.get_db)):
    return UserService.login(form_data, db)


@user_router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.get_user(db, user_id)


@user_router.get("/")
def get_users(db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.get_users(db)


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.delete_user(db, user_id)


@user_router.delete("/")
def delete_all_users(db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.delete_all_users(db)
