#!/usr/bin/env python3

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

class BaseCrawler(object):
    """Danbooru 계열 이미지 수집기
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
        if not check_ini.check_ini(self.config):
            sys.exit(0)
        # 로그 세팅
        if not self._set_logging():
            sys.exit(0)

    def _prepare_crawl(self):
        """수집 준비
        """
        # 이미지 저장 디렉터리 세팅
        if not self._create_save_dir():
            sys.exit(0)
        # 데이터베이스 세팅
        if not self._set_connector_and_cursor():
            sys.exit(0)
        # 요청기 생성
        if not self._set_opener():
            sys.exit(0)

    def start_crawl(self):
        """수집 시작
        """
        self._prepare_crawl()
        # 메타데이터 요청
        metadata = self._get_metadata()
        for posts in metadata:
            for post in posts:
                if not self._is_duplicate(post):
                    self._save_image(post)
                    self._insert_database(post)
                else:
                    self._update_database(post)

    def _insert_database(self, post):
        """데이터베이스에 삽입
        """
        connector = self.connector
        cursor = self.cursor
        post_dict = self._get_post_dict(post)
        query = ('INSERT OR IGNORE INTO image '
               + '(id, created_at, source, md5, rating, '
               + 'tag_string, file_ext, file_url) VALUES ('
               + post_dict['id'] + ', '
               + post_dict['created_at'] + ', '
               + '"' + post_dict['source'] + '", '
               + '"' + post_dict['md5'] + '", '
               + '"' + post_dict['rating'] + '", '
               + '"' + post_dict['tag_string'] + '", '
               + '"' + post_dict['file_ext'] + '", '
               + '"' + post_dict['file_url'] + '")')
        cursor.execute(query)
        connector.commit()
        logging.debug('Query: {0}'.format(query))


    def _update_database(self, post):
        """데이터베이스 업데이트
        """
        connector = self.connector
        cursor = self.cursor
        post_dict = self._set_post_dict(post)
        query = ('UPDATE OR IGNORE image SET '
               + 'created_at=' + post_dict['created_at'] + ', '
               + 'source="' + post_dict['source'] + '", '
               + 'md5="' + post_dict['md5'] + '", '
               + 'rating="' + post_dict['rating'] + '", '
               + 'tag_string="' + post_dict['tag_string'] + '", '
               + 'file_ext="' + post_dict['file_ext'] + '", '
               + 'file_url="' + post_dcit['file_url'] + '" '
               + 'WHERE '
               + 'id=' + post_dict['id'])
        cursor.execute(query)
        connector.commit()
        logging.debug('Query: {0}'.format(query))

    def _get_post_dict(self, post):
        """데이터베이스 업데이트 쿼리 생성
        """
        raise NotImplemented


    def _is_duplicate(self, post):
        """중복된 데이터가 있는지 확인
        인자:
            post: 게시글 데이터
        반환:
            중복있음: True
            중복없음: False
        """
        # 데이터 초기화
        connector = self.connector
        cursor = self.cursor
        post_id = self._parse_id_from_post(post)
        # 중복 확인
        cursor.execute('SELECT * FROM image '
                     + 'WHERE id=' + str(post_id))
        cursor_result = cursor.fetchone()
        if cursor_result != None:
            return True
        else:
            return False
            

    def _parse_id_from_post(self, post):
        """포스트 데이터에서 아이디 추출
        """
        raise NotImplemented

    def _save_image(self, post):
        """이미지 저장
        """
        opener = self.opener
        image_path = self._get_image_path(post)
        image_url = self._get_image_url(post)
        response = opener.open(image_url)
        image_file = open(image_path, 'wb')
        image_file.write(response.read())
        logging.info('저장 완료 {0}'.format(image_path))

    def _get_image_url(self, post):
        """이미지 웹 주소 반환
        """
        raise NotImplemented


    def _get_image_path(self, post):
        """이미지 저장 위치 반환
        """
        raise NotImplemented

    def _get_metadata(self):
        """메타데이터 반환: list of posts
        Generator로 구현하는 것을 추천
        """
        raise NotImplemented


    def _create_save_dir(self):
        config = self.config
        save_dir = config['file']['save_dir']
        try:
            os.makedirs(save_dir, exist_ok = True)
            return True
        except Exception as err:
            logging.critical('_get_image_directory 예외 발생: {0}'.format(
                    err))
            return False
            

    def _set_opener(self):
        """오프너 제작
        """
        raise NotImplemented


    def _set_connector_and_cursor(self):
        config = self.config
        database_name = config['file']['database']
        try:
            connector = sqlite3.connect(database_name)
            cursor = connector.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS image '
                         + '(id INTEGER PRIMARY KEY NOT NULL UNIQUE, '
                         + 'created_at REAL, '
                         + 'source TEXT, '
                         + 'md5 TEXT, '
                         + 'rating TEXT, '
                         + 'tag_string TEXT, '
                         + 'file_ext TEXT, '
                         + 'file_url TEXT)')
            connector.commit()
            (self.connector, self.cursor) = (connector, cursor)
            return True
        except Exception as err:
            logging.critical('__set_logging 예외 발생: {0}'.format(
                    err))
            return False

    def _set_logging(self):
        """로그 시스템 셋업
        """
        config = self.config
        filename = config['log']['file']
        level = config['log']['level']
        level = getattr(logging, level)
        try:
            logging.basicConfig(filename = filename,
                                level = level,
                                format = ('%(asctime)s '
                                        + '%(levelname)s: '
                                        + '%(message)s'),
                                datefmt = '%Y.%m.%d %H:%M:%S')
            return True
        except Exception as err:
            logging.critical('__set_logging 예외 발생: {0}'.format(
                    err))
            return False
