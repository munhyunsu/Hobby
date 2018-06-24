import sys

from example.player import Player
from example.referee import Referee

def main(argv):
    player = Player('사용자')
    computer = Player('컴퓨터', com = True)
    referee = Referee()

    rounds = 0
    while player.win <= 0:
        # 심판의 통제하에 경기 시작!
        rounds = rounds + 1
        referee.go(player, computer)
        print('{0} 라운드 끝!'.format(rounds))

    print('{0}의 승률: {1:.1f}'.format(player.name, player.get_win_ratio()))
    print('{0}의 승률: {1:.1f}'.format(computer.name, computer.get_win_ratio()))


if __name__ == '__main__':
    sys.exit(main(sys.argv))