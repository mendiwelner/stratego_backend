from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from urllib.parse import parse_qs
from fastapi import WebSocket

SECRET_KEY = "secretKey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


class AuthManager:
    @staticmethod
    def extract_token_from_websocket(player_websocket: WebSocket) -> str:
        query_string = player_websocket.scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        return query_params.get("token", [None])[0]

    @staticmethod
    async def verify_token_and_close_websocket(player_websocket: WebSocket, token: str) -> bool:
        if not token or not await AuthManager.verify_token(token):
            await player_websocket.close(code=1008)
            return False
        return True

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def verify_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.utcfromtimestamp(exp):
                raise HTTPException(status_code=401, detail="Token has expired")
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
