#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
import time
from bs4 import BeautifulSoup

def main():
    url = 'http://www.pokemonstore.co.kr/shop/main/index.php'

    print('For exit, press ctrl + c')
    while(True):
        try:
            with urllib.request.urlopen(url) as f:
                if f.code == 200:
                    html = f.read()
                    soup = BeautifulSoup(html, 'html5lib')
                    if soup.title is not None:
                        print(f.code, 'Success', soup.title.text, '\a')
                    else:
                        print(f.code, 'Connected but not html')
        except urllib.error.HTTPError:
            print('May be 404. sleep')
        except KeyboardInterrupt:
            print('pressed ctrl + c. exit')
            break
        time.sleep(60)


if __name__ == '__main__':
    main()
