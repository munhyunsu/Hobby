#!/usr/bin/python3

import configparser
import socket
import sys
import struct
import csv
import time


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

# 스니핑 소켓 생성
# @arg: socket - interface 가 있는 config
def create_socket(config):
    # 설정파일 확인
    if not 'socket' in config:
        print('[FATAL] 설정 파일에 socket 세션이 필요합니다.')
        return None
    if not 'interface' in config['socket']:
        print('[FATAL] 설정 파일 socket 세션에' +
                'interface 항목이 필요합니다.')
        return None
    # 소켓 생성시 예외 발생 가능
    try:
        # 소켓 생성
        read_socket = socket.socket(family=socket.AF_PACKET, \
                type=socket.SOCK_RAW)
        # 인터페이스, 이더넷 종류
        # https://linux.die.net/include/linux/if_ether.h
        socket_interface = (config['arp_request'])['interface']
        socket_ethernet = 0x0004 # Every packet (be careful!!!)
        # 소켓 바인드
        read_socket.bind((socket_interface, socket_ethernet))
    except Exception as err:
        print('[ERROR] create socket 예외 발생')
        return None

    return read_socket


# 맥 주소 파싱
# @arg: 스니핑 소켓
def read_mac_address(read_socket):
    # 읽을 데이터가 없을 떄를 위해 타임 아웃 설정
    read_socket.settimeout(5)
    # 타임 아웃 예외 발생 가능
    try:
        # WLAN 802.11 MTU(2304) + WPA-TKIP(20)
        # https://en.wikipedia.org/wiki/Maximum_transmission_unit
        read_data = read_socket.recv(2324)
        # MAC 주소 파싱
        read_mac = parse_data(read_data)
    except socket.timeout:
        print('[DEBUG] Socket timeout')
        return None
    # MAC 주소 반환
    return read_mac


# Probe Request의 MAC 주소 파싱
def parse_data(read_data):
    # bytes 형만 파싱
    if type(read_data) != bytes:
        print('[ERROR] parse_data 에 주어진 read_data 가 bytes ' +
              '타입이 아닙니다.')
        return None
    # 데이터 커서 생성
    data_cursor = read_data
    if len(data_cursor) < 8:
        return None
    # radiotab header length
    # http://www.radiotap.org/
    radiotab = struct.unpack('!1s1s2s4s', data_cursor[0:8])
    radiotab_length = int.from_bytes(radiotab[2], byteorder='little')
    # 데이터 커서 이동
    data_cursor = data_cursor[radiotab_length:]
    if len(data_cursor) < 22:
        return None
    # 802.11 frame
    frame80211 = struct.unpack('!2s2s6s6s6s', data_cursor[0:22])
    # probe request
    subtype = frame80211[0].hex()
    if subtype[0] != '4':
        return None
    source_mac_address = frame80211[3].hex()
    # MAC 주소 반환
    return source_mac_address

# 메인
def main():
    # 설정파일 불러오기
    config = configparser.ConfigParser()
    config.read('settings.ini')

    # 종료를 위한 try-catch
    try:
        print('기록을 시작합니다.')
        print('중지하시려면 Ctrl + C를 누르세요.')

        # TODO: 소켓 만들기
        read_socket = create_socket(config)
        if read_socket == None:
            print('[FATAL] socket creation fail')
            sys.exit(0)

        # TODO: 데이터 읽기
        while True:
            mac_addr = read_mac_address(read_socket)
            # TODO: 데이터 파싱
            if mac_addr != None:
                continue
            # TODO: 데이터 기록
            
    except KeyboardInterrupt:
        print('기록을 중지합니다.')
        sys.exit(0)

if __name__ == '__main__':
    main()
