from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List
from typing import Tuple

import numpy as np

from game.data_models import Player, Column
from game.game_config import GameConfig


class Condition(ABC):
    def __init__(self, state: List[Column], row: int, col: int):
        self.state = state
        self.last_move = (col, row)

    @abstractmethod
    def check(self, player: Player) -> bool:
        pass

    @staticmethod
    def _check_sequence(sequence: List[str], player: Player) -> bool:
        binary_seq = np.array(list(map(lambda p: 1 if p == player else 0, sequence)))
        win = np.ones(4)
        for i in range(len(sequence) - (len(win) - 1)):
            if sum(binary_seq[i:i + 4] * win) == sum(win):
                return True
        return False

    @staticmethod
    @lru_cache
    def _vertical_slice(last_move: Tuple[int, int]) -> slice:
        low = max(0, last_move[1] - 4)
        high = min(GameConfig.config['board_size']['rows'], last_move[1] + 4)
        return slice(low, high)

    @staticmethod
    @lru_cache
    def _horizontal_slice(last_move: Tuple[int, int]) -> slice:
        left = max(0, last_move[0] - 4)
        right = min(GameConfig.config['board_size']['cols'], last_move[0] + 4)
        return slice(left, right)

    @staticmethod
    def _get_slices(row: List[Player]) -> List[slice]:
        return [slice(i, i + 4) for i in range(len(row) - 4)]
