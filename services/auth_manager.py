from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from db.db_crud.user_crud import UserCRUD

SECRET_KEY = "secretKey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class AuthManager:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def authenticate_user(username: str, password: str, db):
        user = UserCRUD.get_user_by_name(db, username)
        if not user or user.password != password:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    @staticmethod
    def login_user(username: str, password: str, db):
        user = AuthManager.authenticate_user(username, password, db)
        access_token = AuthManager.create_access_token(data={"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}
