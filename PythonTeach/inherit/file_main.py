import sys

import csv

from people import People

def main(argv = sys.argv):
    print_csv()

    select = None
    while select != 0:
        select = print_menu()
        if select == 1:
            add_user()
            print_csv()



def print_menu():
    print('0. 종료')
    print('1. 사용자 추가')
    select = int(input('입력: '))

    return select


def print_csv():
    print('student.csv 내용')
    with open('student.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['name'], row['number'])
    print('student.csv 내용 끝')

    

def add_user():
    print('추가할 사용자 이름과 학번을 입력')
    print('이름과 학번 구분은 공백')
    input_string = input('입력: ')

    (name, number) = input_string.split(' ')

    with open('student.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames = ['name', 'number'])
        #writer.writeheader()
        writer.writerow({'name': name,
                         'number': number})


if __name__ == '__main__':
    sys.exit(main())
