from typing import List

from game.data_models import Player
from .condition import Condition


class ForwardDiagonal(Condition):
    def check(self, player: Player) -> bool:
        diagonal = self._get_diagonal()
        return self._check_sequence(diagonal, player)

    def _get_diagonal(self) -> List[str]:
        vs = self._vertical_slice(self.last_move)
        hs = self._horizontal_slice(self.last_move)
        start = min(vs.stop - self.last_move[1], self.last_move[0] - hs.start) - 1  # left and down
        end = min(self.last_move[1] - vs.start, hs.stop - self.last_move[0])  # right and up
        diagonal = []
        for i in range(-start, end):
            diagonal.append(self.state[self.last_move[0] + i][self.last_move[1] - i])
        return diagonal
