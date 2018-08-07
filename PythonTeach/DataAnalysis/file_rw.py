import sys


def main():
    user_input = None
    user_list = list()
    while user_input != 0:
        print('0. 종료')
        print('1. 사용자 목록 출력')
        print('2. 사용자 추가')
        user_input = int(input('원하는 작업을 선택하세요: '))
        if user_input == 1:
            for entry in user_list:
                print('이름: {이름}, 아이디: {아이디}'.format_map(entry))
        elif user_input == 2:
            name = input('이름: ')
            nick = input('아이디: ')
            user = {'이름': name,
                    '아이디': nick}
            user_list.append(user)

    print('종료합니다.')


if __name__ == '__main__':
    sys.exit(main())
