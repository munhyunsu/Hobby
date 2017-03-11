#!/usr/bin/env python3

import sys # exit, argv
import configparser # configParser
import urllib.request # urlopen
import urllib.parse # urlencode
import base64 # Basic Authorization

INIFILE = 'danboroo.ini'


def main(argv):
    """메인
    """
    config = configparser.ConfigParser()
    config.read(INIFILE)
    # TODO: 설정 파일 확인
    
    url = 'https://danbooru.donmai.us/'
    auth = 'id:key'

    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'Basic ' + 
             base64.b64encode(auth.encode('ascii')).decode('utf-8')
             )]
    with opener.open(url+'posts.json') as f:
        print(f.read().decode('utf-8'))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
