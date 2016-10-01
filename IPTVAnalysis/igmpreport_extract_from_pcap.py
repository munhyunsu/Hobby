#!/usr/bin/python3
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

##### ##### ===== import Area =====
# Agument parse
import sys
# Dir parse
import os
# Fast List or Queue
import collections
# for byte by byte move
import struct
# time parse
import time
# hex to ip
import socket
# ip address
import ipaddress
# json
import json
# Database
#import sqlite3
# DNS parsing
#import binascii
# DNS third-party Lib
#import dnslib
##### ##### ===== import Area End =====






##### ##### ===== Function Area =====
def read_pcap(file_path, json_path):
    packet = open(file_path, 'rb').read()
    magic_number = struct.unpack('!4s2s2s4s4s4s4s', packet[0:24])[0]
    if magic_number == b'\xd4\xc3\xb2\xa1':
        byte_order = 'little'
    else:
        byte_order = 'big'
    print('magic number', '0x' + str(magic_number))
    network_type = struct.unpack('!4s2s2s4s4s4s4s', packet[0:24])[6]
    packet = packet[24:]
    print('pcap capture type:', '0x' + str(network_type))
   
    igmp = dict()
    igmp['user'] = 'LuHa'
    igmp['igmpreports'] = list()
    while(len(packet) > 0):
        time_stamp = ''
        src_address = ''
        des_address = ''
        des_port = 0
        data_size = 0
        http_method = ''
        syn_flag = 0
        fin_flag = 0
        ack_flag = 0

        time_stamp = struct.unpack('!4s4s4s4s', packet[0:16])[0]
        if(magic_number == b'd4c3b2a1'):
            time_stamp = struct.unpack('<I', time_stamp)[0]
        time_stamp = int.from_bytes(time_stamp, byteorder=byte_order)
        time_stamp = time.strftime('%Y.%m.%d. %H:%M:%S', 
                time.localtime(time_stamp))
#        print(time_stamp)
        saved_size = struct.unpack('!4s4s4s4s', packet[0:16])[2]
        if(magic_number == b'd4c3b2a1'):
            saved_size = struct.unpack('<I', saved_size)[0]
        saved_size = int.from_bytes(saved_size, byteorder=byte_order)
#        print('saved_size', saved_size)

        cur_packet = packet[16:]
        packet = packet[saved_size+16:]

        l3_protocol = struct.unpack('!6s6sH', cur_packet[0:14])[2]
        if(l3_protocol != 0x0800):
            continue

        l4_protocol = struct.unpack('!BBHHHBBH4s4s', cur_packet[14:34])[6]
        if(l4_protocol != 0x02):
            continue

        l3_header_size = struct.unpack('!BBHHHBBH4s4s', cur_packet[14:34])[0]
        l3_header_size = (l3_header_size & (0b00001111))
        l3_header_size = l3_header_size * 4
        #print(l3_header_size)

        l3u_size = struct.unpack('!BBHHHBBH4s4s', cur_packet[14:34])[2]
        #print(l3u_size)

        l4_size = l3u_size - l3_header_size
#        print(l4_size)

        data_packet = cur_packet[14+l3_header_size:]

        igmp_type = struct.unpack('BBH4s', data_packet[0:8])[0]
        if(igmp_type != 0x16):
            continue

        multicast_address = struct.unpack('BBH4s', data_packet[0:8])[3]
        multicast_address = ipaddress.IPv4Address(multicast_address)
#        print(ipaddress.IPv4Address(multicast_address))

        print(time_stamp, multicast_address)
        igmp['igmpreports'].append({'timestamp': str(time_stamp), 'groupip': str(multicast_address)})
        #igmp['igmpreports'].append({time_stamp, multicast_address})

#    print(igmp)
    jsonfile = open(json_path, 'w')
    json.dump(igmp, jsonfile, indent = 4, sort_keys = True)
    jsonfile.close()
# End read_pcap()







# Start main()
def main():
    # Get source dir, des file
    if len(sys.argv) < 3:
        print('We need 2 arguments')
        print('.py [PCAPFILE] [JSONFILE]')
        sys.exit()
    file_path = sys.argv[1]
    json_path = sys.argv[2]

    read_pcap(file_path, json_path)
# End main()
##### ##### ===== Function Area End =====


##### script run
if __name__ == '__main__':
    main()





