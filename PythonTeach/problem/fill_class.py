import sys
import random

HANDS = ['가위', '바위', '보']
print(HANDS)


class Player(object):
    FILL_HERE


class Referee(object):
    def go(FILL_HERE):
        home_input = home.get_hands()
        away_input = away.get_hands()
        if away_input == '가위':
            if home_input == '가위':
                home.round_draw()
                away.round_draw()
            elif home_input == '바위':
                home.round_win()
                away.round_lose()
            elif home_input == '보':
                home.round_lose()
                away.round_win()
        elif away_input == '바위':
            if home_input == '가위':
                home.round_lose()
                away.round_win()
            elif home_input == '바위':
                home.round_draw()
                away.round_draw()
            elif home_input == '보':
                home.round_win()
                away.round_lose()
        elif away_input == '보':
            if home_input == '가위':
                home.round_win()
                away.round_lose()
            elif home_input == '바위':
                home.round_lose()
                away.round_win()
            elif home_input == '보':
                home.round_draw()
                away.round_draw()


def main(argv):
    player = FILL_HERE
    computer = FILL_HERE
    referee = FILL_HERE

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
