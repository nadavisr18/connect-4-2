from typing import List

from game.data_models import Column, Move
from .backward_diagonal import BackwardDiagonal
from .condition import Condition
from .forward_diagonal import ForwardDiagonal
from .horizontal import Horizontal
from .vertical import Vertical


class WinConditions:
    @staticmethod
    def get_conditions(state: List[Column], move: Move) -> List[Condition]:
        conditions = [
            BackwardDiagonal,
            ForwardDiagonal,
            Horizontal,
            Vertical
        ]
        return [condition(state=state, row=move.row, col=move.col) for condition in conditions]
