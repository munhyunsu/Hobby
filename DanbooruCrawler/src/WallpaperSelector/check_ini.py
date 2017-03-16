#!/usr/bin/env python3

import configparser # configParser

def check_ini(config):
    """설정 파일 확인
    확인하는 것 들:
        - log
          - level
          - file
    """
    if config['log']['level'] == 'DEBUG':
        return True
    if not 'wallpaper' in config:
        logging.critical('설정 파일에 wallpaper 세션이 '
                       + '필요합니다.')
        return False
    if (not 'path' in config['wallpaper']) or \
            (len(config['wallpaper']['path']) < 1):
        logging.critical('설정 파일 wallpaper 세션에 '
                       + 'path 항목이 필요합니다.')
        return False
    if (not 'number' in config['wallpaper']) or \
            (len(config['wallpaper']['number']) < 1):
        logging.critical('설정 파일 wallpaper 세션에 '
                       + 'number 항목이 필요합니다.')
        return False
    if (not 'map' in config['wallpaper']) or \
            (len(config['wallpaper']['map']) < 1):
        logging.critical('설정 파일 wallpaper 세션에 '
                       + 'map 항목이 필요합니다.')
        return False
    return True
