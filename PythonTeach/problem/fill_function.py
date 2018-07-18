import sys
import random

HANDS = ['가위', '바위', '보']
print(HANDS)


def get_user_input():
    # 사용자 입력
    FILL_HERE


def get_com_input():
    # 컴퓨터 패
    FILL_HERE


def get_result(FILL_HERE):
    result = ''

    # 결과 출력
    if com_input == '가위':
        if user_input == '가위':
            result = '비겼다!'
        elif user_input == '바위':
            result = '플레이어 승리!'
        elif user_input == '보':
            result = '컴퓨터 승리!'
    elif com_input == '바위':
        if user_input == '가위':
            result = '컴퓨터 승리!'
        elif user_input == '바위':
            result = '비겼다!'
        elif user_input == '보':
            result = '플레이어 승리!'
    elif com_input == '보':
        if user_input == '가위':
            result = '플레이어 승리!'
        elif user_input == '바위':
            result = '컴퓨터 승리!'
        elif user_input == '보':
            result = '비겼다!'


def main(argv):
    tried = 0
    result = ''
    while result != '플레이어 승리!':
        # 사용자 입력
        user = get_user_input()

        # 컴퓨터 패
        com = get_com_input()

        # 시도 카운트
        tried = tried + 1

        # 결과 출력
        result = get_result(user, com)
        print(result)

    print('총 {1}판, 승률은! {0:.1f}%'.format(1/tried*100, tried))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
