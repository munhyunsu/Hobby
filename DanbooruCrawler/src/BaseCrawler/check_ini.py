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
    if not 'log' in config:
        logging.critical('설정 파일에 log 세션이 '
                       + '필요합니다.')
        return False
    if (not 'level' in config['log']) or \
            (len(config['log']['level']) < 1):
        logging.critical('설정 파일 log 세션에 '
                       + 'level 항목이 필요합니다.')
        return False
    if (not 'file' in config['log']) or \
            (len(config['log']['file']) < 1):
        logging.critical('설정 파일 log 세션에 '
                       + 'file 항목이 필요합니다.')
        return False
    return True
