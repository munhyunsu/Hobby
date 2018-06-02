import time
import datetime
import urllib.request

def check_internet(max_try = 30, sleep_sec = 1, url = 'https://www.google.com/'):
    for index in range(0, max_try):
        try:
            urllib.request.urlopen(url, timeout = 10)
            return True
        except:
            if index == (max_try-1):
                return False
            print('{0}: Can not reach internet(loop: {1})'.format(datetime.datetime.now(), index+1))
            time.sleep(sleep_sec)
            continue
