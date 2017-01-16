#!/usr/bin/python3

import socket

def main():
    arp_socket = socket.socket(family = socket.AF_PACKET, \
            type = socket.SOCK_RAW)
    arp_socket.setsockopt(socket.SOL_SOCKET, \
            socket.SO_REUSEADDR, 1)
    arp_socket.setsockopt(socket.SOL_SOCKET, \
            socket.SO_BROADCAST, 1)

    arp_socket.settimeout(5)

    arp_socket.bind(('wlp3s0', 0x0806))

    # 메시지를 헥사 형태의 문자열로 입력
    dest_mac = 'ffffffffffff'
    src_mac = ''
    l2_type = '0806' # ARP
    hardware_type = '0001' # Ethernet
    protocol_type = '0800' # IPv4
    hardware_size = '06'
    protocol_size = '04'
    opcode = '0001' # Request
    sender_mac = src_mac
    sender_ip = (socket.inet_aton('192.168.1.')).hex()
    target_mac = '000000000000'
    target_ip = (socket.inet_aton('192.168.1.')).hex()
    
    arp_request = dest_mac + src_mac + l2_type + \
            hardware_type + protocol_type + \
            hardware_size + protocol_size + \
            opcode + \
            sender_mac + sender_ip + target_mac + target_ip
    arp_socket.send(bytes.fromhex(arp_request), 0)

    try:
        arp_reply = arp_socket.recv(1024)
        print(arp_reply.hex())
    except Exception as err:
        print('Timeout {0}'.format(err))


if __name__ == '__main__':
    main()
