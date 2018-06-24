import sys
import random

HANDS = ['가위', '바위', '보']

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

if __name__ == '__main__':
    print('여기는 플레이어 소스코드')