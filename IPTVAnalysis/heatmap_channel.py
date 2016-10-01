#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import datetime
import numpy
import matplotlib.pyplot as plt


def draw_heatmap(input_path, output_path):
    # ready to ploting data
    draw_data = list()
    for index in range(0, 7):
        draw_data.append(list())
    for node in draw_data:
        for index in range(0, 24):
            node.append(numpy.nan)

    #print(draw_data)
    program_json_file = open(input_path, 'r')
    program_json = json.load(program_json_file)
    program_json_file.close()

    # Data assign
    for node in program_json:
        time_now = datetime.datetime.strptime(node['timestamp'], \
                '%Y.%m.%d. %H:%M:%S')
        time_weekday = time_now.weekday()
        time_hour = time_now.hour
        channel_number = int(node['channelnumber'])
        (draw_data[time_weekday])[time_hour] = channel_number

    # draw plot
    #plt.imshow(draw_data, cmap = 'Greys', interpolation = 'nearest')
    #plt.imshow(draw_data, cmap = 'Paired', interpolation = 'nearest', vmin = 0, vmax = 185)
    plt.imshow(draw_data, cmap = 'Paired', interpolation = 'nearest')
    plt.ylabel('Weekdays')
    plt.xlabel('Hours')
    plt.title('What Did I Watch ? Heatmap')
    plt.yticks(range(0, 7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    plt.xticks(range(0, 24), list(range(0, 24)))
    cbar = plt.colorbar(orientation = 'horizontal')
    cbar.set_label('Channel Number')
    #plt.show()
    plt.savefig(output_path, bbox_inches = 'tight')
    plt.close()


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
    draw_heatmap(input_path, output_path)


if __name__ == '__main__':
    main()
