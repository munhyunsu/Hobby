#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json


def remove_unknown_channel(input_path, output_path):
    # read igmp file
    channel_json_file = open(input_path, 'r')
    channel_json = json.load(channel_json_file)
    channel_json_file.close()

    # output list
    viewchannel_json = list()
    for node in channel_json:
        if node['channelnumber'] != '0':
            viewchannel_json.append(node)

    # output file
    viewchannel_json_file = open(output_path, 'w')
    json.dump(viewchannel_json, viewchannel_json_file, \
            ensure_ascii = False, indent = 4, sort_keys = True)
    viewchannel_json_file.close()



def main():
    # Get src, des file
    if len(sys.argv) < 3:
        print('We need 2 arguments')
        print('.py [CHANNELJSON] [OUTPUTFILE]')
        sys.exit()
    # 입출력 파일 경로 지정
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # 본 작업 메소드 호출
    remove_unknown_channel(input_path, output_path)

if __name__ == '__main__':
    main()
