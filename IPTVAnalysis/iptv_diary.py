#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import datetime

def update_diary(iptv_diary_json, info):
    # 프로그램 검색
    for node in iptv_diary_json:
        if (node['programname'] == info['programname']) and \
                (node['channelnumber'] == info['channelnumber']):
            start_datetime = datetime.datetime.strptime( \
                    node['starttime'], '%Y.%m.%d. %H:%M:%S')
            end_datetime = datetime.datetime.strptime( \
                    node['endtime'], '%Y.%m.%d. %H:%M:%S')
            newnode_datetime = datetime.datetime.strptime( \
                    info['timestamp'], '%Y.%m.%d. %H:%M:%S')
            start_diff = start_datetime - newnode_datetime
            start_diff = start_diff.total_seconds()
            end_diff = end_datetime - newnode_datetime
            end_diff = end_diff.total_seconds()
            
            if (abs(start_diff) > 86400) or (abs(end_diff) > 86400):
                continue

            # 시작, 끝 시간
            if (start_diff > 0) and (end_diff > 0):
                node['starttime'] = info['timestamp']
            elif (start_diff < 0) and (end_diff < 0):
                node['endtime'] = info['timestamp']
            # 마무리
            return

    # 프로그램 결과에 따른 분기
    newnode = dict()
    newnode_starttime = datetime.datetime.strptime(info['timestamp'], \
            '%Y.%m.%d. %H:%M:%S')
    newnode_endtime = newnode_starttime + datetime.timedelta(seconds = 1)
    newnode['starttime'] = newnode_starttime.strftime('%Y.%m.%d. %H:%M:%S')
    newnode['endtime'] = newnode_endtime.strftime('%Y.%m.%d. %H:%M:%S')
    newnode['channelname'] = info['channelname']
    newnode['channelnumber'] = info['channelnumber']
    newnode['programname'] = info['programname']
    newnode['programgenre'] = info['programgenre']
    newnode['programage'] = info['programage']
    iptv_diary_json.append(newnode)
    return


def iptv_diary(input_path, output_path):
    # read igmp file
    program_json_file = open(input_path, 'r')
    program_json = json.load(program_json_file)
    program_json_file.close()

    # output list
    iptv_diary_json = list()
    for node in program_json:
        update_diary(iptv_diary_json, node)

    # Write to json
    iptv_diary_json_file = open(output_path, 'w')
    json.dump(iptv_diary_json, iptv_diary_json_file, ensure_ascii= False, \
            indent = 4, sort_keys = True)
    iptv_diary_json_file.close()
    #print(iptv_diary_json)
        


def main():
    # Get src, des file
    if len(sys.argv) < 3:
        print('We need 2 arguments')
        print('.py [PROGRAMJSON] [OUTPUTFILE]')
        sys.exit()
    # 입출력 파일 경로 지정
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # 본 작업 메소드 호출
    iptv_diary(input_path, output_path)

if __name__ == '__main__':
    main()
