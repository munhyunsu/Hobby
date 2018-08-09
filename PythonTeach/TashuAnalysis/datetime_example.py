import datetime


def main():
    date_str = '20180811162445'
    date_format = datetime.datetime.strptime(date_str, '%Y%m%d%H%M%S')
    print(date_format, date_format.weekday())

    date_str = '2018-08-11 16:24:45'
    date_format = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    print(date_format, date_format.weekday())


if __name__ == '__main__':
    main()