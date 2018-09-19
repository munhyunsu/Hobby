import time
import random

from chocolate_jar import ChocolateJar


def show_jar(jar):
    chocolates = jar.chocolates
    print('■', end='')
    for index in range(0, chocolates-1):
        print('□', end='')
    print('')


def main():
    jar = ChocolateJar(13)
    print('게임을 시작합니다.')
    print('항아리에 {0}개의 초콜릿와 1개의 고추가 있습니다.'.format(13))
    print('1~3개의 초콜릿 혹은 고추를 꺼낼 수 있으며 고추를 꺼내면 패배합니다.')
    print('시작!')
    show_jar(jar)
    turn = 1
    while jar.chocolates > 0:
        print('----+ {0}번 턴! ----+'.format(turn))
        take = input('몇 개의 초콜릿을 뺄까요?: ')
        take = int(take.strip())
        print('플레이어는 {0}개의 초콜릿을 꺼냈습니다.'.format(take))
        jar.take_chocolate(take)
        show_jar(jar)
        if jar.chocolates == 1:
            print('플레이어 승리!')
            break

        max_take = min(jar.chocolates - 1, 3)
        take = random.randint(1, max_take)
        print('컴퓨터 고민중...', end=' ')
        time.sleep(take)
        print('컴퓨터는 {0}개의 초콜릿을 꺼냈습니다.'.format(take))
        jar.take_chocolate(take)
        show_jar(jar)
        if jar.chocolates == 1:
            print('컴퓨터 승리!')
            break
        turn = turn+1


if __name__ == '__main__':
    main()
