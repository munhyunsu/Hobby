#!/usr/bin/env python3

import check_ini

import sys # exit, argv
import logging # 로깅
import configparser # configParser
import shutil # copyfile

class BaseSelector(object):
    """배경화면 복사 기본 클래스
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

    def start_copy(self):
        """복사 시작
        """
        self._prepare_copy()
        # 위치 요청
        paths = self._get_path()
        for (src_path, dst_path) in paths:
            shutil.copyfile(src_path, dst_path)
            logging.info('복사 완료 {0}'.format(dst_path))
            
    def _prepare_copy(self):
        """복사 준비
        1. 목표 위치 생성 및 비우기
        2. 각종 변수 초기화
        """
        raise NotImplemented
