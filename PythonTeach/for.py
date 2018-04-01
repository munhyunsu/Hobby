def main():
    for index in range(0, 10):
        print('{0}'.format(index))

    answer = int(input('다음 숫자는? '))

    if answer == 10:
        print('정답입니다!\n')
    else:
        print('오답입니다...\n')

main()
