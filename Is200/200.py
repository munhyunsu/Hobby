#!/usr/bin/env python3

# exit, argv
import sys
# request
import urllib.request
# sleep
import time

# target url
TARGET = 'http://www.pokemonstore.co.kr/'

def main(argv):
    """
    request looping
    """
    # for arguments
    if len(argv) > 1:
        target = argv[1]
    else:
        target = TARGET

    # main loop
    while(True):
        try:       
            with urllib.request.urlopen(target) as f:
                if f.code == 200:
                    print('[200 OK] from {0}'.format(target))
                else:
                    print('[Error] from {0}'.format(target))
            time.sleep(30)
        except KeyboardInterrupt:
            print('Good shopping')
            break
        except urllib.error.URLError:
            print('Website not exist')
            time.sleep(10)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
