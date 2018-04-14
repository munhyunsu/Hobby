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
print(user_input, com_input, sep = ' vs ')
