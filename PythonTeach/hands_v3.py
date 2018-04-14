import sys
import random

HANDS = ['가위', '바위', '보']
print(HANDS)

tried = 0
while True:
    # 사용자 입력
    user_input = input('입력하세요: ')
    user_input = user_input.strip()
    if user_input not in HANDS:
        print('입력값이 이상합니다.')
        break

    # 컴퓨터 패
    com_input = random.choice(HANDS)

    # 시도 카운트
    tried = tried + 1

    # 결과 출력
    if com_input == '가위':
        if user_input == '가위':
            result = '비겼다!'
        elif user_input == '바위':
            result = '플레이어 승리!'
            break
        elif user_input == '보':
            result = '컴퓨터 승리!'
    elif com_input == '바위':
        if user_input == '가위':
            result = '컴퓨터 승리!'
        elif user_input == '바위':
            result = '비겼다!'
        elif user_input == '보':
            result = '플레이어 승리!'
            break
    elif com_input == '보':
        if user_input == '가위':
            result = '플레이어 승리!'
            break
        elif user_input == '바위':
            result = '컴퓨터 승리!'
        elif user_input == '보':
            result = '비겼다!'
    print(result)

print('마지막판 플레이어 승리로 승률은! {0:.1f}%'.format(1/tried*100))
