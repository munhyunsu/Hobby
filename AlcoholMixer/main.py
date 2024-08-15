import logging

FLAGS = _ = None



def menu() -> str:
    print('---------- Menu ----------')
    print('| 1. 토닉을 얼마나 타지?')
    print('| Q. 종료')
    print('-------------------------')

    selected = input('사용자 입력: ')

    return selected


def calc_v2():
    print('기준이 되는 술의 양을 입력해주세요 (ml).')
    v1 = float(input('사용자 입력: '))
    print('기준이 되는 술의 도수를 입력해주세요.')
    c1 = float(input('사용자 입력: '))



def main():
    logging.critical('Critical message example')
    logging.error('Error message example')
    logging.warning('Warning message example')
    logging.info('Info message example')
    logging.debug('Debug message example')

    while True:
        selected = menu().upper()
        logging.info(f'사용자 입력 {selected}')
        if selected == 'Q':
            print('종료합니다.')
            break
        elif selected == '1':
            logging.debug('1번 선택')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', default='WARNING',
                        choices=logging._nameToLevel.keys(),
                        help='Set log level (default: WARNING)')

    FLAGS, _ = parser.parse_known_args()
    logging.basicConfig(level=FLAGS.logging)

    main()

