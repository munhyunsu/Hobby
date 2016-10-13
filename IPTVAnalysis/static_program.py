#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import datetime


def top_contents(input_path):
    diary_file = open(input_path, 'r')
    diary_json = json.load(diary_file)
    diary_file.close()

    content_number = dict()
    content_hour = dict()
    
    for node in diary_json:
        content_number[node['programname']] = \
                content_number.get(node['programname'], 0) + 1

        start_datetime = datetime.datetime.strptime( \
                node['starttime'], '%Y.%m.%d. %H:%M:%S')
        end_datetime = datetime.datetime.strptime( \
                node['endtime'], '%Y.%m.%d. %H:%M:%S')
        during_time = end_datetime - start_datetime

        content_hour[node['programname']] = \
                content_hour.get(node['programname'], 0) + \
                during_time.total_seconds() / 3600

    print('가장 많이 본 컨텐츠!')
    for top in sorted(content_number, key = content_number.get, \
            reverse = True):
        print(top, ': ', content_number[top], '회')

    print('가장 오랫동안 본 컨텐츠!')
    for top in sorted(content_hour, key = content_hour.get, \
            reverse = True):
        print(top, ': ', content_hour[top], '시간')


def main():
    # Get src, des file
    if len(sys.argv) < 2:
        print('We need 1 arguments')
        print('.py [DIARYJSON]')
        sys.exit()
    # 입출력 파일 경로 지정
    input_path = sys.argv[1]

    # 본 작업 메소드 호출
    top_contents(input_path)


if __name__ == '__main__':
    main()
