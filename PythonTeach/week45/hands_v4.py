import sys
import random

HANDS = ['가위', '바위', '보']
print(HANDS)


def get_user_input():
    # 사용자 입력
    user_input = input('입력하세요: ')
    user_input = user_input.strip()
    if user_input not in HANDS:
        print('입력값이 이상합니다.')
        sys.exit(0)
    return user_input



def get_com_input():
    # 컴퓨터 패
    com_input = random.choice(HANDS)
    return com_input



def get_result(user_input, com_input):
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
    return result


def main(argv):
    tried = 0
    result = ''
    while result != '플레이어 승리!':
        # 사용자 입력
        #user_input = get_user_input()
        user = get_user_input()

        # 컴퓨터 패
        #com_input = get_com_input()
        com = get_com_input()

        # 시도 카운트d
        tried = tried + 1

        # 결과 출력
        #result = get_result(user_input, com_input)
        result = get_result(user, com)
        print(result)

    print('총 {1}판, 승률은! {0:.1f}%'.format(1/tried*100, tried))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
