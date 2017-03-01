#!/usr/bin/python3

import configparser
import sys
import os
import logging
import sqlite3
import urllib.parse # urlunparse
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler
import time

class ClassScannerServerHandler(CGIHTTPRequestHandler):
    # 초기화
    # ini 파일 위치 확인
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = 'classscanserver.ini'
    if not os.path.exists(config_file):
        logging.critical('Config file does not exists: {0}'.format(
                         config_file))
        sys.exit(0)
    config = configparser.ConfigParser()
    config.read(config_file)
    # ini 핸들 옵션
    if not 'handle' in config:
        logging.critical('설정 파일에 handle 세션이 필요합니다.')
        sys.exit(0)
    if not 'database' in config['handle']:
        logging.critical('설정 파일 handle 세션에 '
                        + 'database 항목이 필요합니다.')
        sys.exit(0)
    # 내부 변수
    database_file = config['handle']['database']
    # 저장할 데이터베이스 생성
    connector = sqlite3.connect(database_file)
    cursor = connector.cursor()
    cursor.executescript('''
            CREATE TABLE IF NOT EXISTS classscan
            ( number INTEGER PRIMARY KEY AUTOINCREMENT,
            unix_time INTEGER,
            identifier TEXT,
            scanned_mac TEXT );
            ''')
    connector.commit()

    # POST
    def do_POST(self):
        # 홈페이지
        if self.path != '/':
            CGIHTTPRequestHandler.do_POST(self)
            return
        # 응답 전송
        self.send_response(200)
        self.end_headers()
        try:
            # 전송받은 데이터 파싱
            data = self.rfile.read()
            data = data.decode('utf-8')
            data = urllib.parse.parse_qs(data)
            # 저장할 데이터 준비
            unix_time = int(time.time())
            identifier = data['identifier'][0]
            log_set = data['log_set'][0]
            # 데이터베이스 커밋
            self.cursor.execute('''
                    INSERT OR IGNORE INTO classscan
                    (unix_time, identifier, scanned_mac) VALUES ('''
                    + str(unix_time) + ', '
                    + '"' + identifier + '", '
                    + '"' + log_set + '")')
            self.connector.commit()
            # 성공 응답 전송
            self.send_response(202)
            self.end_headers()
        except Exception as err:
            logging.error(err)
            # 실패 응답 전송
            self.send_response(400)
            self.end_headers()

    # print nothing!
    def log_message(self, format, *args):
        logging.debug('{0} {1} {2}'.format(
                     self.client_address, self.command, self.path))
        return

def main():
    """HTTP 서버 데몬 생성
    """
    # ini 파일 위치 확인
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = 'classscanserver.ini'
    if not os.path.exists(config_file):
        logging.critical('Config file does not exists: {0}'.format(
                         config_file))
        sys.exit(0)
    config = configparser.ConfigParser()
    config.read(config_file)
    # ini 서버 옵션
    if not 'server' in config:
        logging.critical('설정 파일에 server 세션이 필요합니다.')
        sys.exit(0)
    if not 'port' in config['server']:
        logging.critical('설정 파일 server 세션에 '
                        + 'port 항목이 필요합니다.')
        sys.exit(0)
    # 변수 생성
    http_port = int(config['server']['port'])
    # ini 로그 옵션
    if not 'log' in config:
        logging.critical('설정 파일에 log 세션이 필요합니다.')
        sys.exit(0)
    if not 'level' in config['log']:
        logging.critical('설정 파일 log 세션에 '
                        + 'level 항목이 필요합니다.')
        sys.exit(0)
    if not 'file' in config['log']:
        logging.critical('설정 파일 log 세션에 '
                        + 'file 항목이 필요합니다.')
        sys.exit(0)
    # 로그 레벨, 파일 이름 불러오기
    log_level = getattr(logging, config['log']['level'])
    log_file = config['log']['file']
    # 로그 레벨 세팅
    logging.basicConfig(filename = log_file,
                        level = log_level,
                        format = '%(asctime)s '
                               + '%(levelname)s:'
                               + '%(message)s',
                        datefmt = '%Y.%m.%d %H:%M:%S')
    # HTTP 데몬 생성
    try:
        logging.info('서버를 시작합니다. 중지하려면 Ctrl+C를 누르세요.')
        class_scanner_server = HTTPServer(('', http_port),
                                          ClassScannerServerHandler)
        class_scanner_server.serve_forever()
    except KeyboardInterrupt:
        logging.info('서버를 중지합니다.')

if __name__ == '__main__':
    main()

