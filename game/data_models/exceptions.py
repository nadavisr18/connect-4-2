from .player import Player


class ColumnFullException(Exception):
    def __init__(self, column: int):
        self.column = column
        self.message = f"Column {column} is full"
        super().__init__(self.message)


class SamePlayerException(Exception):
    def __init__(self, player: Player):
        self.player = player
        self.message = f"Player {player} Tried to Play Twice in a Row"
        super().__init__(self.message)
