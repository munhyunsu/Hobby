import os
import sys
import signal
import time
import subprocess

WHO = None


def handler(signum, frame):
    global WHO
    print('Signal handler', signum, WHO, frame)
    print('Disable handler', signum, WHO, frame)
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def main(argv):
    global WHO
    WHO = argv[1]
    if WHO == 'parent':
        signal.signal(signal.SIGINT, handler)
        p = subprocess.Popen('python3 signal_propagation.py child',
                             shell=True,
                             restore_signals=True)
        #p = subprocess.Popen('python3 signal_propagation.py child',
        #                     shell=True,
        #                     start_new_session=True)
        #p = subprocess.Popen(['python3', 'signal_propagation.py', 'child'])
        #p = subprocess.Popen(['/bin/bash', '-c', 'python3 signal_propagation.py child'])

    for index in range(0, 4):
        time.sleep(1)
        print('Sleep', index, WHO)
    
    if WHO == 'parent':
        #os.killpg(os.getpgid(p.pid), signal.SIGINT)
        p.send_signal(signal.SIGINT)
        #while True:
        #    time.sleep(1)
        #    print('Sleep 1 inf parent')
        p.communicate()
    else:
        while True:
            time.sleep(1)
            print('Sleep 1 infinity')

if __name__ == '__main__':
    main(sys.argv)

