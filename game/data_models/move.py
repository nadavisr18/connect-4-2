from pydantic import BaseModel

from .player import Player


class Move(BaseModel):
    row: int
    col: int
    player: Player
