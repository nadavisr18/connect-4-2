from pydantic import BaseModel, field_validator

from game.data_models import Player


class Move(BaseModel):
    column: int
    player: Player

    @field_validator('column')
    def column_must_be_valid(cls, v):
        if not (0 <= v <= 6):
            raise ValueError('Column must be between 0 and 6')
        return v
