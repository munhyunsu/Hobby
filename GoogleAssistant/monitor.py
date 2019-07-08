import shlex
import subprocess
import time

def watch(fn, words, stop):
    go = False
    fp = open(fn, 'r')
    while True:
        new = fp.readline()
        # Once all lines are read this just returns ''
        # until the file changes and a new line appears
        if stop in new:
            go = True
            print('turn on')
        if go and words in new:
            go = False
            print('return')
            yield new


def execute():
    command = './start_sample.sh'
    command_line = shlex.split(command)
    p = subprocess.Popen(command_line, shell=True)
    return p

def kill():
    command = 'killall start_sample.sh'
    command_line = shlex.split(command)
    subprocess.run(command_line)
    command = 'killall googlesamples-assistant-pushtotalk'
    command_line = shlex.split(command)
    subprocess.run(command_line)


fn = 'out'
words = '"how\'s the weather".'
stop = 'Recording audio request.'
subprocess.run(['rm', 'out'])
subprocess.run(['touch', 'out'])
execute()
for new in watch(fn, words, stop):
    print('Found', new)
    kill()
    subprocess.run(['mpv', '--loop-playlist=no', '--keep-open=no', 'weather.mp3'])
    print('sleep 1')
    time.sleep(1)
    execute()

