from cProfile import Profile

from game import Board
from game.data_models import Player


def main(moves=None):
    board = Board()
    player = Player.X
    while True:
        col = input(f"Enter column for {player}: ")
        board.insert(int(col), player)
        board.display()
        if board.check_win():
            print(f"{player} Won!!!")
            break
        player = Player.O if player == Player.X else Player.X


def profile():
    p = Profile()
    p.enable()
    moves = [6, 5, 5, 4, 3, 4, 4, 2, 3, 3, 3]
    for i in range(1000):
        main(moves)
    p.disable()
    p.print_stats(2)


if __name__ == '__main__':
    main()
