user_input = None
user_list = list()
while user_input != 0:
    print('0. 종료')
    print('1. 사용자 목록 출력')
    print('2. 사용자 추가')
    user_input = int(input('원하는 작업을 선택하세요: '))
    if user_input == 1:
        print(user_list)
    elif user_input == 2:
        name = input('이름: ')
        id = input('아이디: ')
        user = {'이름': name,
                '아이디': id}
        user_list.append(user)


print('종료합니다.')
