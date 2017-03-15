#!/usr/bin/env python3

from BaseCrawler import base_crawler
import check_ini

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

INIFILE = 'yandere.ini'

class YandereRandomCrawler(base_crawler.BaseCrawler):
    """Yandere 이미지 랜덤 다운로더
    """
    def __init__(self, config_file):
        """초기화 함수
        """
        # 부모 클래스 초기화
        base_crawler.BaseCrawler.__init__(self, config_file)
        # 입력 파일 확인
        if type(config_file) == dict:
            self.config = config_file
        else:
            self.config = configparser.ConfigParser()
            self.config.read(config_file)
        # 설정 파일 확인
        if not check_ini.check_ini(self.config):
            sys.exit(0)

    def _set_opener(self):
        """요청기 생성
        """
        try:
            config = self.config
            user_id = config['authorization']['user_id']
            api_key = config['authorization']['api_key']
            # HTTP 기본 인증
            # base64로 데이터를 보내야 함
            # 'login:api_key' 형태
            authorization_basic = user_id + ':' + api_key
            authorization_basic = authorization_basic.encode('ascii')
            authorization_basic = base64.b64encode(authorization_basic)
            authorization_basic = authorization_basic.decode('utf-8')
            self.opener = urllib.request.build_opener()
            self.opener.addheaders = [('Authorization', 
                    'Basic ' + authorization_basic)]
            return True
        except Exception as err:
            logging.critical('_set_opener 예외 발생 {0}'.format(
                    err))
            return False
            
    def _get_metadata(self):
        """메타데이터 반환
        Generator
        """
        config = self.config
        url = config['crawl']['url']
        tags = config['crawl']['tags']
        tags = tags.splitlines()
        loop_number = int(config['crawl']['loop_number'])
        opener = self.opener
        for tag in tags:
            for index in range(0, loop_number):
                logging.info('태그 수집: {0} {1}'.format(
                        tag, index+1))
                request_url = (url + '/post.json?tags='
                             + tag + '+order:random')
                response = opener.open(request_url)
                posts = json.loads(response.read().decode('utf-8'))
                yield posts

    def _parse_id_from_post(self, post):
        """포스트 데이터에서 게시글 아이디 추출
        """
        try:
            return post['id']
        except Exception as err:
            logging.critical('_parse_id_from_post 예외 발생 {0}'.format(
                    err))
            sys.exit(0)

    def _get_image_path(self, post):
        """이미지 저장 위치 반환
        """
        config = self.config
        save_dir = config['file']['save_dir']
        try:
            image_path = (save_dir + '/'
                        + post['md5'] + '.' + post['file_ext'])
            return image_path
        except Exception as err:
            logging.critical('_get_image_path 예외 발생 {0}'.format(
                    err))
            sys.exit(0)
            
    def _get_image_url(self, post):
        """이미지 웹 주소 반환
        """
        config = self.config
        try:
            image_url = post['file_url']
            return image_url
        except Exception as err:
            logging.critical('_get_image_url 예외 발생 {0}'.format(
                    err))
            sys.exit(0)

    def _get_post_dict(self, post):
        try:
            # 데이터베이스 변수
            post_dict = dict()
            post_dict['id'] = str(post['id'])
            post_created_at = float(post['created_at'])
            post_dict['created_at'] = str(post_created_at)
            post_dict['source'] = str(post['source'])
            post_dict['md5'] = str(post['md5'])
            post_dict['rating'] = str(post['rating'])
            post_tag_string = str(post['tags'])
            post_dict['tag_string'] = post_tag_string.replace('\"', '\'')
            post_dict['file_ext'] = str(post['file_ext'])
            post_dict['file_url'] = str(post['file_url'])
            return post_dict
        except Exception as err:
            logging.critical('_get_post_dict 예외 발생 {0}'.format(
                    err))
            sys.exit(0)

def main(argv):
    yandere_random = YandereRandomCrawler(INIFILE)
    yandere_random.start_crawl()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
