#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json

def analysis_igmpreport(igmp_json_path, channel_json_path):
    # Group ID Read from file
    # TODO(LuHa): 추후 sqlite로 전환할 것
    group_ip_file = open('group_ip.json', 'r')
    group_ip = json.load(group_ip_file)
    group_ip_file.close()

    # igmp file read
    igmp_json_file = open(igmp_json_path, 'r')
    igmp_json = json.load(igmp_json_file)
    igmp_json_file.close()

    # set output file
    channel_json = list()
    for report in igmp_json['igmpreports']:
        try:
            report['channelnumber'] = str(group_ip[report['groupip']]['number'])
            report['channelname'] = group_ip[report['groupip']]['name']
        except:
            report['channelnumber'] = str(0)
            report['channelname'] = 'Unknown'
        channel_json.append(report)

    # 채널정보 닫기
    channel_json_file = open(channel_json_path, 'w')
    json.dump(channel_json, channel_json_file, ensure_ascii = False, indent = 4, sort_keys = True)
    channel_json_file.close()

    #print(channel_json)


        
    





def main():
    # Get src, des file
    if len(sys.argv) < 3:
        print('We need 2 arguments')
        print('.py [IGMPJSONFILE] [OUTPUTJSONFILE]')
        sys.exit()
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    analysis_igmpreport(input_path, output_path)

if __name__ == '__main__':
    main()
