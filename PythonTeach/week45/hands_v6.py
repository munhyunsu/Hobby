import sys
import random

HANDS = ['가위', '바위', '보']
print(HANDS)


class Player(object):
    def __init__(self, name, com = False):
        self.name = name
        self.com = com
        self.win = 0
        self.lose = 0
        self.draw = 0

    def get_hands(self):
        if self.com == True:
            return random.choice(HANDS)
        # 사용자 입력
        user_input = input('입력하세요: ')
        user_input = user_input.strip()
        if user_input not in HANDS:
            print('입력값이 이상합니다.')
            sys.exit(0)
        return user_input

    def round_win(self):
        self.win = self.win + 1

    def round_lose(self):
        self.lose = self.lose + 1

    def round_draw(self):
        self.draw = self.draw + 1

    def get_win_ratio(self):
        return (self.win) / (self.win + self.lose + self.draw)



class Referee(object):
    def __init__(self):
        self.rounds = 0

    def go(self, home, away):
        self.rounds = self.rounds + 1
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
    player = Player('사용자')
    computer = Player('컴퓨터', com = True)
    referee = Referee()

    for index range(0, 10):
        # 심판의 통제하에 경기 시작!
        referee.go(player, computer)
        print('{0} 라운드 끝!'.format(referee.rounds))

    print('{0}의 승률: {1:.1f}'.format(player.name, player.get_win_ratio()))
    print('{0}의 승률: {1:.1f}'.format(computer.name, computer.get_win_ratio()))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
