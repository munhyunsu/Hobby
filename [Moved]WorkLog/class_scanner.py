#!/usr/bin/python3

from base_scanner import MACScanner
import logging # log
import sys # exit
import time # group mac
import urllib.parse # urlencode
import urllib.request # urlopen

class ClassMACScanner(MACScanner):
    """주위에서 읽은 MAC 주소를 출력 클래스
    """
    # 초기화
    def __init__(self, config_file):
        # 부모 클래스 초기화
        MACScanner.__init__(self, config_file)
        # ini 파일 확인
        if not 'handle' in self.config:
            logging.critical('설정 파일에 handle 세션이 필요합니다.')
            sys.exit(0)
        if not 'time' in self.config['handle']:
            logging.critical('설정 파일 handle 세션에 '
                             + 'time 항목이 필요합니다.')
            sys.exit(0)
        if not 'url' in self.config['handle']:
            logging.critical('설정 파일 handle 세션에 '
                             + 'url 항목이 필요합니다.')
            sys.exit(0)
        if not 'identifier' in self.config['handle']:
            logging.critical('설정 파일 handle 세션에 '
                             + 'identifier 항목이 필요합니다.')
            sys.exit(0)
        # 내부 변수 초기화
        self.last_handle = int(time.time())
        self.log_set = set()
        self.handle_time = int(self.config['handle']['time'])
        self.url = self.config['handle']['url']
        self.identifier = self.config['handle']['identifier']
        
    # 데이터 전송
    def _send_log(self):
        # 데이터 시리얼화
        send_data = {'identifier': self.identifier,
                     'log_set': self.log_set}
        send_data = urllib.parse.urlencode(send_data) # URL 형태로 변환
        send_data = send_data.encode('ascii') # bytes 로 변환
        send_request = urllib.request.Request(self.url, data = send_data)
        try:
            with urllib.request.urlopen(send_request) as response:
                logging.debug('Send {0} MAC. Status: {1}'.format(
                              len(self.log_set), response.status))
        except Exception as err:
            logging.error('MAC address send error: {0}'.format(err))

    # MAC 주소 다루기
    def _handle_mac(self, mac):
        # 시간 비교용 변수
        now_handle = int(time.time())
        # 저장 셋에 추가
        self.log_set.add(mac.upper())
        # 일정 시간마다 저장
        if (now_handle - self.last_handle) > self.handle_time:
            # TODO: 세트 전송
            self._send_log()
            # 다음 저장 시간 세팅 및 변수 클리어
            self.last_handle = now_handle
            self.log_set.clear()

def main():
    config_file = 'classscan.ini'
    mac_scanner = ClassMACScanner(config_file)
    mac_scanner.start_scan()

if __name__ == '__main__':
    main()
