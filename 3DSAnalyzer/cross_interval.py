#!/usr/bin/python3
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
##### ##### ===== import Area End =====






##### ##### ===== Function Area =====
def read_pcap(file_path):
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
   
    
    time_stamp_before = 0
    time_stamp_after = 0
    while(len(packet) > 0):
        time_stamp = struct.unpack('!4s4s4s4s', packet[0:16])[0]
        time_stamp_msec = struct.unpack('!4s4s4s4s', packet[0:16])[1]

        if(magic_number == b'd4c3b2a1'):
            time_stamp = struct.unpack('<I', time_stamp)[0]
            time_stamp_msec = struct.unpack('<I', time_stamp_msec)[0]

        time_stamp = int.from_bytes(time_stamp, byteorder=byte_order)
        time_stamp_msec = int.from_bytes(time_stamp_msec, 
                byteorder=byte_order)
        time_stamp_msec = time_stamp_msec / 1000000
        time_stamp_all = time_stamp + time_stamp_msec

        time_stamp_before = time_stamp_after
        time_stamp_after = time_stamp_all

        time_diff = time_stamp_after - time_stamp_before

        print(time_diff)

        saved_size = struct.unpack('!4s4s4s4s', packet[0:16])[2]
        if(magic_number == b'd4c3b2a1'):
            saved_size = struct.unpack('<I', saved_size)[0]
        saved_size = int.from_bytes(saved_size, byteorder=byte_order)
        packet = packet[saved_size+16:]

# End read_pcap()







# Start main()
def main():
    # Get source pcap
    if len(sys.argv) < 2:
        print('We need 1 arguments')
        print('.py [PCAPFILE]')
        sys.exit()
    file_path = sys.argv[1]

    read_pcap(file_path)
# End main()
##### ##### ===== Function Area End =====


##### script run
if __name__ == '__main__':
    main()
