from typing import List

from game.data_models import Player
from .condition import Condition


class Vertical(Condition):
    def check(self, player: Player) -> bool:
        vertical = self._get_vertical()
        return self._check_sequence(vertical, player)

    def _get_vertical(self) -> List[str]:
        vs = self._vertical_slice(self.last_move)
        vertical = self.state[self.last_move[0]][vs]
        return vertical
