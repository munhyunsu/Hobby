#!/usr/bin/env python3

import os # chmod
import sys # exit, argv
import logging # 로깅
import configparser # configParser
import urllib.request # urlopen
import urllib.parse # urlencode
import base64 # Basic Authorization
import sqlite3 # SQL
import time # sleep
import json # json loads
import datetime # datetime.strptime

INIFILE = 'danbooru.ini'


def main(argv):
    """메인
    """
    # 설정 불러오기
    config = configparser.ConfigParser()
    config.read(INIFILE)
    # 설정 파일 확인
    if not 'authorization' in config:
        logging.critical('설정 파일에 authorization 세션이 '
                       + '필요합니다.')
        sys.exit(0)
    if (not 'url' in config['authorization']) or \
            (len(config['authorization']['url']) < 1):
        logging.critical('설정 파일 authorization 세션에 '
                       + 'url 항목이 필요합니다.')
        sys.exit(0)
    if (not 'user_id' in config['authorization']) or \
            (len(config['authorization']['user_id']) < 1):
        logging.critical('설정 파일 authorization 세션에 '
                       + 'user_id 항목이 필요합니다.')
        sys.exit(0)
    if (not 'api_key' in config['authorization']) or \
            (len(config['authorization']['api_key']) < 1):
        logging.critical('설정 파일 authorization 세션에 '
                       + 'api_key 항목이 필요합니다.')
        sys.exit(0)
    if not 'crawl' in config:
        logging.critical('설정 파일에 crawl 세션이 '
                       + '필요합니다.')
        sys.exit(0)
    if (not 'tags' in config['crawl']) or \
            (len(config['crawl']['tags']) < 1):
        logging.critical('설정 파일 crawl 세션에 '
                       + 'tags 항목이 필요합니다.')
        sys.exit(0)
    if (not 'loop_number' in config['crawl']) or \
            (len(config['crawl']['loop_number']) < 1):
        logging.critical('설정 파일 crawl 세션에 '
                       + 'loop_number 항목이 필요합니다.')
        sys.exit(0)
    if (not 'sleep_time' in config['crawl']) or \
            (len(config['crawl']['sleep_time']) < 1):
        logging.critical('설정 파일 crawl 세션에 '
                       + 'sleep_time 항목이 필요합니다.')
        sys.exit(0)
    if not 'file' in config:
        logging.critical('설정 파일에 file 세션이 '
                       + '필요합니다.')
        sys.exit(0)
    if (not 'database' in config['file']) or \
            (len(config['file']['database']) < 1):
        logging.critical('설정 파일 file 세션에 '
                       + 'database 항목이 필요합니다.')
        sys.exit(0)
    if (not 'save_dir' in config['file']) or \
            (len(config['file']['save_dir']) < 1):
        logging.critical('설정 파일 file 세션에 '
                       + 'save_dir 항목이 필요합니다.')
        sys.exit(0)
    if not 'log' in config:
        logging.critical('설정 파일에 log 세션이 '
                       + '필요합니다.')
        sys.exit(0)
    if (not 'level' in config['log']) or \
            (len(config['log']['level']) < 1):
        logging.critical('설정 파일 log 세션에 '
                       + 'level 항목이 필요합니다.')
        sys.exit(0)
    if (not 'file' in config['log']) or \
            (len(config['log']['file']) < 1):
        logging.critical('설정 파일 log 세션에 '
                       + 'file 항목이 필요합니다.')
        sys.exit(0)
    # 로그 세팅
    log_level = getattr(logging, config['log']['level'])
    log_file = config['log']['file']
    logging.basicConfig(filename = log_file,
                        level = log_level,
                        format = '%(asctime)s '
                               + '%(levelname)s: '
                               + '%(message)s',
                        datefmt = '%Y.%m.%d %H:%M:%S')
    # 데이터베이스 세팅
    database_name = config['file']['database']
    connector = sqlite3.connect(database_name)
    #os.chmod(database_name, 0o666)
    cursor = connector.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS image '
                 + '(id INTEGER PRIMARY KEY NOT NULL UNIQUE, '
                 + 'created_at REAL, '
                 + 'source TEXT, '
                 + 'md5 TEXT, '
                 + 'rating TEXT, '
                 + 'tag_string TEXT, '
                 + 'file_url TEXT)')
    connector.commit()
    logging.debug('Database 연결 완료')
    # 쿼리 준비
    url = config['authorization']['url']
    user_id = config['authorization']['user_id']
    api_key = config['authorization']['api_key']
    tags = config['crawl']['tags'].splitlines()
    loop_number = int(config['crawl']['loop_number'])
    sleep_time = int(config['crawl']['sleep_time'])
    # 요청기 생성
    authorization_basic = user_id + ':' + api_key
    authorization_basic = authorization_basic.encode('ascii')
    authorization_basic = base64.b64encode(authorization_basic)
    authorization_basic = authorization_basic.decode('utf-8')
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'Basic ' + authorization_basic)]
    logging.debug('요청기 생성 완료')
    # 이미지 저장 위치 생성
    save_dir = config['file']['save_dir']
    os.makedirs(save_dir, exist_ok = True)
    logging.debug('저장 디렉터리 생성 완료')
    # 쿼리 전송
    for tag in tags:
        for index in range(0, loop_number):
            logging.info('태그 시작 {0} : {1}'.format(tag, index+1))
            response = opener.open(url
                                 + '/posts.json?tags='
                                 + tag 
                                 + '&random=true')
            posts = json.loads(response.read().decode('utf-8'))
            for post in posts:
                cursor.execute('SELECT * FROM image '
                             + 'WHERE id=' + str(post['id']))
                cursor_result = cursor.fetchone()
                if cursor_result == None:
                    file_url = post['file_url']
                    img = opener.open(url+file_url)
                    img_file = open(save_dir
                                  + '/' 
                                  + file_url.split('/')[-1], 'wb')
                    img_file.write(img.read())
                    logging.info('저장완료 {0}'.format(img_file))
                # 데이터베이스 변수
                post_id = str(post['id'])
                post_created_at = post['created_at']
                post_created_at = datetime.datetime.strptime(
                        post_created_at[:-3] + post_created_at[-2:],
                        '%Y-%m-%dT%H:%M:%S.%f%z')
                post_created_at = str(post_created_at.timestamp())
                post_source = str(post['source'])
                post_md5 = str(post['md5'])
                post_rating = str(post['rating'])
                post_tag_string = str(post['tag_string'])
                post_file_url = str(post['file_url'])
                # 데이터베이스 저장
                cursor.execute('UPDATE OR IGNORE image SET '
                             + 'created_at=' + post_created_at + ', '
                             + 'source="' + post_source + '", '
                             + 'md5="' + post_md5 + '", '
                             + 'rating="' + post_rating + '", '
                             + 'tag_string="' + post_tag_string + '", '
                             + 'file_url="' + post_file_url + '" '
                             + 'WHERE '
                             + 'id=' + post_id)
                cursor.execute('INSERT OR IGNORE INTO image '
                             + '(id, created_at, source, md5, rating, '
                             + 'tag_string, file_url) VALUES ('
                             + post_id + ', '
                             + post_created_at + ', '
                             + '"' + post_source + '", '
                             + '"' + post_md5 + '", '
                             + '"' + post_rating + '", '
                             + '"' + post_tag_string + '", '
                             + '"' + post_file_url + '")')
                connector.commit()
                logging.debug('데이터베이스 저장 완료')
                time.sleep(sleep_time)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
