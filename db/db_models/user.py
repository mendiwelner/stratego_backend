from typing import Dict

from sqlalchemy import Column, Integer, String, Boolean
from .base import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String, index=True)
    setup = Column(String, index=True)
    rating = Column(Integer, index=True)
    is_active = Column(Boolean, index=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "setup": self.setup,
            "rating": self.rating,
            "is_active": self.is_active
        }