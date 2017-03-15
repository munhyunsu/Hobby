#!/usr/bin/env python3

import configparser # configParser

def check_ini(config):
    """설정 파일 확인
    확인하는 것 들:
        - authorization
          - user_id
          - api_key
        - crawl
          - url
          - tags
          - loop_number
          - sleep_time
        - file
          - database
          - save_dir
    """
    if config['log']['level'] == 'DEBUG':
        return True
    if not 'authorization' in config:
        logging.critical('설정 파일에 authorization 세션이 '
                       + '필요합니다.')
        return False
    if (not 'user_id' in config['authorization']) or \
            (len(config['authorization']['user_id']) < 1):
        logging.critical('설정 파일 authorization 세션에 '
                       + 'user_id 항목이 필요합니다.')
        return False
    if (not 'api_key' in config['authorization']) or \
            (len(config['authorization']['api_key']) < 1):
        logging.critical('설정 파일 authorization 세션에 '
                       + 'api_key 항목이 필요합니다.')
        return False
    if not 'crawl' in config:
        logging.critical('설정 파일에 crawl 세션이 '
                       + '필요합니다.')
        return False
    if (not 'url' in config['crawl']) or \
            (len(config['crawl']['url']) < 1):
        logging.critical('설정 파일 crawl 세션에 '
                       + 'url 항목이 필요합니다.')
        return False
    if (not 'tags' in config['crawl']) or \
            (len(config['crawl']['tags']) < 1):
        logging.critical('설정 파일 crawl 세션에 '
                       + 'tags 항목이 필요합니다.')
        return False
    if (not 'loop_number' in config['crawl']) or \
            (len(config['crawl']['loop_number']) < 1):
        logging.critical('설정 파일 crawl 세션에 '
                       + 'loop_number 항목이 필요합니다.')
        return False
    if not 'file' in config:
        logging.critical('설정 파일에 file 세션이 '
                       + '필요합니다.')
        return False
    if (not 'database' in config['file']) or \
            (len(config['file']['database']) < 1):
        logging.critical('설정 파일 file 세션에 '
                       + 'database 항목이 필요합니다.')
        return False
    if (not 'save_dir' in config['file']) or \
            (len(config['file']['save_dir']) < 1):
        logging.critical('설정 파일 file 세션에 '
                       + 'save_dir 항목이 필요합니다.')
        return False
    return True
