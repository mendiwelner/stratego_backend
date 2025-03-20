from sqlalchemy import Column, Integer

from .base import Base


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
