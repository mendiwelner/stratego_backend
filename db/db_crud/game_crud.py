from sqlalchemy.orm import Session
from db.db_models.game import Game


class GameCRUD:
    @staticmethod
    def get_game(db: Session, game_id: int):
        return db.query(Game).filter(Game.id == game_id).first()

    @staticmethod
    def get_games(db: Session):
        return db.query(Game).all()

    @staticmethod
    def create_game(db: Session, game_name: str):
        new_game = Game(name=game_name)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return new_game

