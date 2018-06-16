import sys
import random

HANDS = ['가위', '바위', '보']
print(HANDS)

# 사용자 입력
user_input = input('입력하세요: ')
user_input = user_input.strip()
if user_input not in HANDS:
    print('입력값이 이상합니다.')
    sys.exit(0)

# 컴퓨터 패
com_input = random.choice(HANDS)

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

print('가위, 바위, 보! {0}'.format(result))
