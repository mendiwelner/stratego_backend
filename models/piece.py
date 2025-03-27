from pydantic import BaseModel


class Piece(BaseModel):
    number_of_player: int
    value: str

    def __str__(self):
        return f"{self.value[0]}"

    @staticmethod
    def create(player: int, value: str):
        return Piece(number_of_player=player, value=value)

    def to_dict(self):
        return {
            "number_of_player": self.number_of_player,
            "value": self.value
        }

    def return_losers_in_attack(self, in_to_cell: "Piece") -> int:
        if in_to_cell.value == "b":
            if self.value == "3":
                return 2
            else:
                return 1
        elif in_to_cell.value == "f":
            return 2
        elif self.value == in_to_cell.value:
            return 0
        elif self.value == "1" and in_to_cell.value == "10":
            return 2
        else:
            if int(self.value) > int(in_to_cell.value):
                return 2
            else:
                return 1
