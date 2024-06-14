from typing import List

from game.data_models import Player
from .condition import Condition


class Horizontal(Condition):
    def check(self, player: Player) -> bool:
        horizontal = self._get_horizontal()
        return self._check_sequence(horizontal, player)

    def _get_horizontal(self) -> List[str]:
        hs = self._horizontal_slice(self.last_move)
        horizontal = [col[self.last_move[1]] for col in self.state[hs]]
        return horizontal
