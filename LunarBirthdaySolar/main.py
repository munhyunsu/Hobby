import csv
import datetime
import os
import urllib.parse
import urllib.request
from xml.etree import ElementTree

import secret

ENDPOINT = 'http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getSolCalInfo'
FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed: {FLAGS}')
        print(f'Unparsed: {_}')
    print(' 이름  (   음력   ) ==>  올해양력 ')
    with open(FLAGS.target, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name']
            birthday = datetime.date.fromisoformat(row['Birthday'])
            try:
                data = {'lunYear': FLAGS.year,
                        'lunMonth': f'{birthday.month:02d}',
                        'lunDay': f'{birthday.day:02d}',
                        'serviceKey': secret.key}
                data = urllib.parse.urlencode(data)
                url = f'{ENDPOINT}?{data}'
                with urllib.request.urlopen(url) as req:
                    res = req.read().decode('utf-8')
                    root = ElementTree.fromstring(res)
                    solar = (f'{root.findall("*//solYear")[0].text}-'
                             f'{root.findall("*//solMonth")[0].text}-'
                             f'{root.findall("*//solDay")[0].text}')
                    solar = datetime.date.fromisoformat(solar)
                print(f'{name} ({birthday}) ==> {solar}')
            # TODO(LuHa): IndexError 가 2가지 원인으로 나타남
            ## 1. 윤달이 생일인 경우! (기존 버전 코드)
            ## 2. API 사용 권한이 만료된 경우!! (이거 개선 필요!!)
            except IndexError: # Minor calandar!
                birthday = birthday - datetime.timedelta(days=1)
                data = {'lunYear': FLAGS.year,
                        'lunMonth': f'{birthday.month:02d}',
                        'lunDay': f'{birthday.day:02d}',
                        'serviceKey': secret.key}
                data = urllib.parse.urlencode(data)
                url = f'{ENDPOINT}?{data}'
                with urllib.request.urlopen(url) as req:
                    res = req.read().decode('utf-8')
                    root = ElementTree.fromstring(res)
                    solar = (f'{root.findall("*//solYear")[0].text}-'
                             f'{root.findall("*//solMonth")[0].text}-'
                             f'{root.findall("*//solDay")[0].text}')
                    solar = datetime.date.fromisoformat(solar)
                print(f'{name} ({birthday}) ==> {solar} (-1 Day)')
            except Exception as e:
                if DEBUG:
                    print(f'[ERROR] {url} => {e}')


if __name__ == '__main__':
    root_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(root_path)
    os.chdir(root_dir)

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='enable debug mode')
    parser.add_argument('--target', default='sample.csv',
                        help='Birthday csv file')
    parser.add_argument('--year', default=datetime.datetime.now().year,
                        help='Target year')
    FLAGS, _ = parser.parse_known_args()

    FLAGS.config = os.path.abspath(os.path.expanduser(FLAGS.target))

    DEBUG = FLAGS.debug

    main()

