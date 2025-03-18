from pydantic import BaseModel


class CellClickRequest(BaseModel):
    row: int
    col: int
