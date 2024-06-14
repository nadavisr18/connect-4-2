from typing import List, Union

from .cell import Cell
from .player import Player


class Column:
    def __init__(self, rows: int):
        self.state: List[Union[Player, Cell]] = [Cell.EMPTY.value] * rows
        self.next_empty: int = rows - 1

    def __getitem__(self, item: int):
        return self.state[item]

    def __len__(self) -> int:
        return len(self.state)

    def insert(self, player: Player):
        self.state[self.next_empty] = player
        self.next_empty -= 1
