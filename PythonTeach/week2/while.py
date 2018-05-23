def main():
    index = 0
    while index < 10:
        print('{0}'.format(index))
        index = index+1

    answer = int(input('다음 숫자는? '))

    if answer == 10:
        print('정답입니다!\n')
    else:
        print('오답입니다...\n')

main()
