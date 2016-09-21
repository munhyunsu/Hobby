#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import datetime
import urllib.request
from bs4 import BeautifulSoup

def get_program(timestamp, channelnumber):
    # convert string to time
    stime = time.strptime(timestamp, '%Y.%m.%d. %H:%M:%S')
    
    # construct url
    channel_url = 'http://tv.olleh.com/renewal_sub/liveTv/\
pop_schedule_week.asp?ch_no=' + channelnumber + '&nowdate=' + \
time.strftime('%Y%m%d', stime)

    print(channel_url)
    # check channel directory exist?
    file_dir = './channel_htmls/'
    #file_path = file_dir + channel_url
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    # check chnnel file exist?
    file_path = file_dir + channelnumber + '_' + time.strftime('%Y%m%d', stime) + '.html'
    if not os.path.exists(file_path): # If not, download channel info.
        time.sleep(3)
        response = urllib.request.urlopen(channel_url)
        html = response.read()
        html_file = open(file_path, 'w')
        html_file.write(html.decode('euc-kr'))
        html_file.close()

    # open channel information html
    channel_dict = dict()
    html_file = open(file_path, 'r')
    soup = BeautifulSoup(html_file, 'html5lib')
    table = soup.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        channel_dict[ time.strftime('%Y.%m.%d.', stime) + ' ' + \
                cols[0] + ':00' ] = cols

    time_now = datetime.datetime.strptime(timestamp, \
            '%Y.%m.%d. %H:%M:%S')
    time_now = time_now - datetime.timedelta(seconds = time_now.second)
    time_now = time_now - datetime.timedelta(minutes = time_now.minute%10)
    for index in range(0, 1440, 10):
        if time_now.strftime('%Y.%m.%d. %H:%M:%S') in channel_dict:
            match_channel = channel_dict[time_now.strftime('%Y.%m.%d. %H:%M:%S')]

            return (match_channel[1], match_channel[2], match_channel[4])
            break
        else:
            time_now = time_now - datetime.timedelta(minutes = 10)
        
    return (None, None, None)


def program_analysis(input_path, output_path):
    # read igmp file
    viewchannel_json_file = open(input_path, 'r')
    viewchannel_json = json.load(viewchannel_json_file)
    viewchannel_json_file.close()

    # output list
    program_json = list()
    for node in viewchannel_json:
        (program_name, program_age, program_genre) = \
                get_program(node['timestamp'], node['channelnumber'])
        node['programname'] = program_name
        node['programage'] = program_age
        node['programgenre'] = program_genre
        
        program_json.append(node)

    # Write to json
    program_json_file = open(output_path, 'w')
    json.dump(program_json, program_json_file, ensure_ascii= False, \
            indent = 4, sort_keys = True)
    program_json_file.close()
        



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
    program_analysis(input_path, output_path)

if __name__ == '__main__':
    main()
