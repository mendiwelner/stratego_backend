import json
from models.piece import Piece


class PieceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Piece):
            # Serialize the Piece object using its `to_dict` method
            return obj.to_dict()
        return super().default(obj)
