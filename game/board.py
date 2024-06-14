from typing import List, Tuple

from game.data_models import Column, Move, Player, \
    ColumnFullException, SamePlayerException
from .game_config import GameConfig
from .win_conditions import WinConditions


class Board:
    def __init__(self):
        self.state: List[Column] = []
        for i in range(GameConfig.COLS):
            self.state.append(Column(GameConfig.ROWS))

        self.last_move: Move = Move(row=-1, col=-1, player=Player.O)

    def get_json(self) -> List[List[str]]:
        board = []
        for r in range(len(self.state[0])):
            row = []
            for c in range(len(self.state)):
                row.append(self.state[c][r])
            board.append(row)
        return board

    def insert(self, col: int, player: Player):
        self._verify_insert(col, player)
        row = self.state[col].next_empty
        self.state[col].insert(player)
        self.last_move = Move(row=row, col=col, player=player)

    def check_win(self) -> Tuple[bool, Player]:
        if self.last_move.col == -1:
            return False, Player.EMPTY
        win = False
        for condition in WinConditions.get_conditions(self.state, self.last_move):
            win |= condition.check(self.last_move.player)
        return win, self.last_move.player

    def display(self):
        board = ""
        for row in range(len(self.state[0])):
            for col in range(len(self.state)):
                board += f"|{self.state[col][row]}"
            board += "|\n"
        print(board)

    def _verify_insert(self, col: int, player: Player):
        if self.state[col].next_empty == -1:
            raise ColumnFullException(col)
        if not self.last_move.col == -1 and self.last_move.player == player:
            raise SamePlayerException(player)
