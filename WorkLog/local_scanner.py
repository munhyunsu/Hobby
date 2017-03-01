#!/usr/bin/python3

from base_scanner import MACScanner
import time
import sqlite3

class LocalMACScanner(MACScanner):
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
        if not 'database' in self.config['handle']:
            logging.critical('설정 파일 handle 세션에 '
                             + 'database 항목이 필요합니다.')
            sys.exit(0)
        # 내부 변수 초기화
        self.last_handle = int(time.time())
        self.log_set = set()
        self.handle_time = int(self.config['handle']['time'])
        # 저장할 데이터베이스 생성
        self.connector = sqlite3.connect(self.config['handle']['database'])
        self.cursor = self.connector.cursor()
        self.cursor.executescript('''
                CREATE TABLE IF NOT EXISTS localscan
                ( unix_time INTEGER PRIMARY KEY NOT NULL UNIQUE,
                scanned_mac TEXT );
                ''')
        self.connector.commit()

    # MAC 주소 다루기
    def _handle_mac(self, mac):
        # 시간 비교용 변수
        now_handle = int(time.time())
        # 저장 셋에 추가
        self.log_set.add(mac.upper())
        # 일정 시간마다 저장
        if (now_handle - self.last_handle) > self.handle_time:
            # 데이터베이스 커밋
            self.cursor.execute('''
                    INSERT OR IGNORE INTO localscan
                    (unix_time, scanned_mac) VALUES ('''
                    + str(now_handle) + ', '
                    + '"' + str(self.log_set) + '")')
            self.connector.commit()
            # 다음 저장 시간 세팅 및 변수 클리어
            self.last_handle = now_handle
            self.log_set.clear()

def main():
    config_file = 'localscan.ini'
    mac_scanner = LocalMACScanner(config_file)
    mac_scanner.start_scan()

if __name__ == '__main__':
    main()
