#!/usr/bin/python3

import socket
import struct
import csv
import time
import configparser


def read_member_dict_from_file():
    member_dict = dict()

    config = configparser.ConfigParser()
    config.read('settings.ini')
    for mac in config['members']:
        member_dict[mac.lower()] = (config['members'])[mac]

    return member_dict



def get_alive_member(member_dict):
    alive_member = set()

    config = configparser.ConfigParser()
    config.read('settings.ini')

    arp_socket = socket.socket(family = socket.AF_PACKET, \
            type = socket.SOCK_RAW)
    arp_socket.setsockopt(socket.SOL_SOCKET, \
            socket.SO_REUSEADDR, 1)
    arp_socket.setsockopt(socket.SOL_SOCKET, \
            socket.SO_BROADCAST, 1)
    arp_socket.settimeout(5)

    
    arp_interface = (config['arp_request'])['interface']
    arp_socket.bind((arp_interface, 0x0806))

    # 메시지를 헥사 형태의 문자열로 입력
    dest_mac = 'ffffffffffff'
    src_mac = (config['arp_request'])['src_mac']
    l2_type = '0806' # ARP
    hardware_type = '0001' # Ethernet
    protocol_type = '0800' # IPv4
    hardware_size = '06'
    protocol_size = '04'
    opcode = '0001' # Request
    sender_mac = (config['arp_request'])['src_mac']
    sender_ip = (config['arp_request'])['src_ip']
    sender_ip = (socket.inet_aton(sender_ip)).hex()
    for index in range(0, 256):
        target_mac = '000000000000'
        target_ip = '192.168.1.' + str(index)
        target_ip = (socket.inet_aton(target_ip)).hex()
    
        arp_request = dest_mac + src_mac + l2_type + \
                hardware_type + protocol_type + \
                hardware_size + protocol_size + \
                opcode + \
                sender_mac + sender_ip + target_mac + target_ip
        arp_socket.send(bytes.fromhex(arp_request), 0)

    try:
        for index in range(0, 1024):
            arp_reply = arp_socket.recv(1024)
            arp_struct = struct.unpack('@6s6s2s2s2s1s1s2s6s4s6s4s', \
                    arp_reply[:42])
            if arp_struct[10].hex() == sender_mac:
                if arp_struct[8].hex() in member_dict:
                    alive_member.add(member_dict[arp_struct[8].hex()])
    except socket.timeout:
        pass
    except Exception as err:
        print('Exception: {0}'.format(err))

    arp_socket.close()

    return alive_member

        
def write_csv_log(alive_member):
    if len(alive_member) == 0:
        return

    with open('alive.csv', 'a', newline = '') as csvfile:
        alive_writer = csv.writer(csvfile, \
                delimiter = ',', quotechar = '"', \
                quoting = csv.QUOTE_ALL)
        alive_writer.writerow([time.ctime(), alive_member])
    


def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    try:
        print('기록을 시작합니다.')
        print('중지하시려면 Ctrl + C를 누르세요.')
        while True:
            member_dict = read_member_dict_from_file()

            alive_member = get_alive_member(member_dict)

            write_csv_log(alive_member)

            time.sleep( \
                    int( \
                            (config['main'])['sleep_time'] \
                    )
            )
    except KeyboardInterrupt:
        print('기록을 중지합니다.')

if __name__ == '__main__':
    main()
