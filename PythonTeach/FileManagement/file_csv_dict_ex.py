import csv


def main():
    with open('names.csv', 'w') as f:
        fieldnames = ['성', '이름']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'성': '문', '이름': '현수'})
        writer.writerow({'성': '홍', '이름': '길동'})

    with open('names.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)


    print('----- 절취선 -----')

    with open('names.csv', 'a') as f:
        fieldnames = ['성', '이름']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows([{'성': '이', '이름': '형진'}, {'성': '민', '이름': '지원'}])

    with open('names.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)


if __name__ == '__main__':
    main()