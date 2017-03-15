#!/usr/bin/env python3

import os # makedirs
import sys # exit, argv
import logging # 로깅
import configparser # configParser
import sqlite3 # SQL
import shutil # copyfile

INIFILE = 'wallpaper_selector.ini'

class WallpaperSelector(object):
    """배경화면 복사
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
        # 로그 레벨, 파일 이름 불러오기
        log_level = getattr(logging, self.config['log']['level'])
        log_file = self.config['log']['file']
        # 로그 레벨 세팅
        logging.basicConfig(filename = log_file,
                            level = log_level,
                            format = '%(asctime)s '
                                   + '%(levelname)s: '
                                   + '%(message)s',
                            datefmt = '%Y.%m.%d %H:%M:%S')
        # 구간 생성
        path = self.config['wallpaper']['path']
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok = True)
        logging.info('목표 디렉터리 생성 완료 {0}'.format(path))

    def _check_config(self):
        # TODO: path 설정
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

    def copy_wallpaper(self):
        wallpaper_path = self.config['wallpaper']['path']
        wallpaper_number = str(self.config['wallpaper']['number'])
        wallpaper_map = \
                self.config['wallpaper']['map'].splitlines()

        for map_line in wallpaper_map:
            (database, image) = map_line.split(' ')
            connector = sqlite3.connect(database)
            cursor = connector.cursor()
            cursor.execute('SELECT file_url FROM image '
#                         + 'WHERE '
#                         + 'rating="s" '
                         + 'ORDER BY RANDOM() '
                         + 'LIMIT ' + wallpaper_number)
            cursor_result = cursor.fetchall()
            for (file_path,) in cursor_result:
                src_path = image + '/' + file_path.split('/')[-1]
                dst_path = wallpaper_path + '/' + file_path.split('/')[-1]
                shutil.copyfile(src_path, dst_path)
                logging.info(dst_path)




def main(argv):
    wallpaper_selector = WallpaperSelector(INIFILE)
    wallpaper_selector.copy_wallpaper()



if __name__ == '__main__':
    sys.exit(main(sys.argv))
