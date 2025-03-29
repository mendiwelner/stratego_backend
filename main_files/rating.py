from typing import List

from db.db_crud.user_crud import UserCRUD
from main_files.player import Player
from db.db_manager.db_session_manager import DBSessionManager
from sqlalchemy.orm import Session


class Rating:
    @staticmethod
    def update_players_rating(players: List[Player], loser: int):
        k = 30
        player_1_rating = players[0].rating
        player_2_rating = players[1].rating

        if loser == 3:
            winner_rating_change = k * (0.5 - Rating.calculate_expectation(player_1_rating, player_2_rating))
            loser_rating_change = k * (0.5 - Rating.calculate_expectation(player_2_rating, player_1_rating))
            players[0].rating += winner_rating_change
            players[1].rating += loser_rating_change
        elif loser == 1:
            Rating.update_rating_for_loser(players, player_1_rating, player_2_rating, k, winner_is=2)
        elif loser == 2:
            Rating.update_rating_for_loser(players, player_2_rating, player_1_rating, k, winner_is=1)

        players[0].rating = round(players[0].rating)
        players[1].rating = round(players[1].rating)

        Rating.update_user_rating(players[0].player_name, players[0].rating)
        Rating.update_user_rating(players[1].player_name, players[1].rating)

    @staticmethod
    def update_rating_for_loser(players: List[Player], winner_rating: int, loser_rating: int, k: int, winner_is: int):
        winner_rating_change = k * (1 - Rating.calculate_expectation(loser_rating, winner_rating))
        loser_rating_change = k * (0 - Rating.calculate_expectation(winner_rating, loser_rating))

        if winner_is == 1:
            players[0].rating += winner_rating_change
            players[1].rating += loser_rating_change
        elif winner_is == 2:
            players[1].rating += winner_rating_change
            players[0].rating += loser_rating_change

    @staticmethod
    def update_user_rating(player_name: str, rating: int, db: Session = DBSessionManager.get_db()) -> dict:
        return UserCRUD.update_user_rating(db, player_name, rating)

    @staticmethod
    def calculate_expectation(rating_a: int, rating_b: int):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
