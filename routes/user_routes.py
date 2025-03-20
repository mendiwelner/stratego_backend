from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.db_crud.user_crud import UserCRUD
from db.db_manager.db_session_manager import DBSessionManager

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/")
def create_new_user(name: str, email: str, db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.create_user(db, name, email)


@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.get_user(db, user_id)


@router.get("/")
def get_users(db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.get_users(db)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.delete_user(db, user_id)


@router.delete("/")
def delete_all_users(db: Session = Depends(DBSessionManager.get_db)):
    return UserCRUD.delete_all_users(db)
