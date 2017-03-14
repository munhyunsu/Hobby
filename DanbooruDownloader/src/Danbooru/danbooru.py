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

class DanbooruCrawler(object):
    """Danbooru 계열 이미지 랜덤 다운로더
    """
    def __init__(self, config_file):
        """설정 파일 입력 받기
        """
        # 입력 파일 확인
        if type(config_file) == dict:
            self.config = config_file
        else:
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
        # 설정 파일 확인
        self._check_config()
        # 로그 세팅
        log_level = getattr(logging, self.config['log']['level'])
        log_file = self.config['log']['file']
        logging.basicConfig(filename = log_file,
                            level = log_level,
                            format = '%(asctime)s '
                                   + '%(levelname)s: '
                                   + '%(message)s',
                            datefmt = '%Y.%m.%d %H:%M:%S')
        # 데이터베이스 세팅
        database_name = self.config['file']['database']
        self.connector = sqlite3.connect(database_name)
        self.cursor = self.connector.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS image '
                         + '(id INTEGER PRIMARY KEY NOT NULL UNIQUE, '
                         + 'created_at REAL, '
                         + 'source TEXT, '
                         + 'md5 TEXT, '
                         + 'rating TEXT, '
                         + 'tag_string TEXT, '
                         + 'file_url TEXT)')
        self.connector.commit()
        logging.debug('Database 연결 완료')
        # 요청기 생성
        user_id = self.config['authorization']['user_id']
        api_key = self.config['authorization']['api_key']
        authorization_basic = user_id + ':' + api_key
        authorization_basic = authorization_basic.encode('ascii')
        authorization_basic = base64.b64encode(authorization_basic)
        authorization_basic = authorization_basic.decode('utf-8')
        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [('Authorization', 
                'Basic ' + authorization_basic)]
        logging.debug('요청기 생성 완료')
        # 이미지 저장 디렉터리 생성
        self.save_dir = self.config['file']['save_dir']
        os.makedirs(self.save_dir, exist_ok = True)
        #logging.debug('저장 디렉터리 생성 완료')

    def _check_config(self):
        if not 'authorization' in self.config:
            logging.critical('설정 파일에 authorization 세션이 '
                           + '필요합니다.')
            sys.exit(0)
        if (not 'user_id' in self.config['authorization']) or \
                (len(self.config['authorization']['user_id']) < 1):
            logging.critical('설정 파일 authorization 세션에 '
                           + 'user_id 항목이 필요합니다.')
            sys.exit(0)
        if (not 'api_key' in self.config['authorization']) or \
                (len(self.config['authorization']['api_key']) < 1):
            logging.critical('설정 파일 authorization 세션에 '
                           + 'api_key 항목이 필요합니다.')
            sys.exit(0)
        if not 'crawl' in self.config:
            logging.critical('설정 파일에 crawl 세션이 '
                           + '필요합니다.')
            sys.exit(0)
        if (not 'url' in self.config['crawl']) or \
                (len(self.config['crawl']['url']) < 1):
            logging.critical('설정 파일 crawl 세션에 '
                           + 'url 항목이 필요합니다.')
            sys.exit(0)
        if (not 'tags' in self.config['crawl']) or \
                (len(self.config['crawl']['tags']) < 1):
            logging.critical('설정 파일 crawl 세션에 '
                           + 'tags 항목이 필요합니다.')
            sys.exit(0)
        if (not 'loop_number' in self.config['crawl']) or \
                (len(self.config['crawl']['loop_number']) < 1):
            logging.critical('설정 파일 crawl 세션에 '
                           + 'loop_number 항목이 필요합니다.')
            sys.exit(0)
        if (not 'sleep_time' in self.config['crawl']) or \
                (len(self.config['crawl']['sleep_time']) < 1):
            logging.critical('설정 파일 crawl 세션에 '
                           + 'sleep_time 항목이 필요합니다.')
            sys.exit(0)
        if not 'file' in self.config:
            logging.critical('설정 파일에 file 세션이 '
                           + '필요합니다.')
            sys.exit(0)
        if (not 'database' in self.config['file']) or \
                (len(self.config['file']['database']) < 1):
            logging.critical('설정 파일 file 세션에 '
                           + 'database 항목이 필요합니다.')
            sys.exit(0)
        if (not 'save_dir' in self.config['file']) or \
                (len(self.config['file']['save_dir']) < 1):
            logging.critical('설정 파일 file 세션에 '
                           + 'save_dir 항목이 필요합니다.')
            sys.exit(0)
        if not 'log' in self.config:
            logging.critical('설정 파일에 log 세션이 '
                           + '필요합니다.')
            sys.exit(0)
        if (not 'level' in self.config['log']) or \
                (len(self.config['log']['level']) < 1):
            logging.critical('설정 파일 log 세션에 '
                           + 'level 항목이 필요합니다.')
            sys.exit(0)
        if (not 'file' in self.config['log']) or \
                (len(self.config['log']['file']) < 1):
            logging.critical('설정 파일 log 세션에 '
                           + 'file 항목이 필요합니다.')
            sys.exit(0)

    def _crawl_image(self, tag):
        """이미지 다운로드 시작
        """
        url = self.config['crawl']['url']
        sleep_time = int(self.config['crawl']['sleep_time'])
        response = self.opener.open(url
                             + '/posts.json?tags='
                             + tag 
                             + '&random=true')
        posts = json.loads(response.read().decode('utf-8'))
        for post in posts:
            self.cursor.execute('SELECT * FROM image '
                         + 'WHERE id=' + str(post['id']))
            cursor_result = self.cursor.fetchone()
            image_path = post['md5'] + '.' + post['file_ext']
            if cursor_result == None:
                img = self.opener.open(url+post['file_url'])
                img_file = open(self.save_dir
                              + '/' 
                              + image_path, 'wb')
                img_file.write(img.read())
                logging.info('저장 완료 {0}'.format(image_path))
            else:
                logging.info('중복 패스 {0}'.format(image_path))
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
            post_tag_string = post_tag_string.replace('\"', '\'')
            #logging.debug('tag: {0}'.format(post_tag_string))
            post_file_url = str(post['file_url'])
            # 데이터베이스 저장
            query = ('UPDATE OR IGNORE image SET '
                    + 'created_at=' + post_created_at + ', '
                    + 'source="' + post_source + '", '
                    + 'md5="' + post_md5 + '", '
                    + 'rating="' + post_rating + '", '
                    + 'tag_string="' + post_tag_string + '", '
                    + 'file_url="' + post_file_url + '" '
                    + 'WHERE '
                    + 'id=' + post_id)
            logging.debug('Query: {0}'.format(query))
            self.cursor.execute(query)
            query = 'INSERT OR IGNORE INTO image '
                  + '(id, created_at, source, md5, rating, '
                  + 'tag_string, file_url) VALUES ('
                  + post_id + ', '
                  + post_created_at + ', '
                  + '"' + post_source + '", '
                  + '"' + post_md5 + '", '
                  + '"' + post_rating + '", '
                  + '"' + post_tag_string + '", '
                  + '"' + post_file_url + '")')
            logging.debug('Query: {0}'.format(query))
            self.cursor.execute(query)
            self.connector.commit()
            #logging.debug('데이터베이스 저장 완료')
            time.sleep(sleep_time)

    def start_crawl(self):
        tags = self.config['crawl']['tags'].splitlines()
        loop_number = int(self.config['crawl']['loop_number'])
        for tag in tags:
            for index in range(0, loop_number):
                logging.info('태그 시작 {0} : {1}'.format(tag, index+1))
                self._crawl_image(tag)


def main(argv):
    danbooru = DanbooruCrawler(INIFILE)
    danbooru.start_crawl()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
