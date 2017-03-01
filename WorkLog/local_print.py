#!/usr/bin/python3

from base_scanner import MACScanner

class PrintMACScanner(MACScanner):
    """주위에서 읽은 MAC 주소를 출력 클래스
    """
    def _handle_mac(self, mac):
        print(mac.upper())


def main():
    config_file = 'settings.ini'
    mac_scanner = PrintMACScanner(config_file)
    mac_scanner.start_scan()

if __name__ == '__main__':
    main()
