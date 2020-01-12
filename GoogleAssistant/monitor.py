import shlex
import subprocess
import time
import re

from phue import Bridge
b = Bridge('192.168.1.221')
b.connect()


def play_time(_):
    now = time.localtime()
    subprocess.run(['mpv', '--loop-playlist=no', '--keep-open=no', 
                    'numbers/{0}.wav'.format(now.tm_hour),
                    'numbers/{0}.wav'.format(now.tm_min)])


def watch(fn, words, stop):
    go = False
    fp = open(fn, 'r')
    while True:
        new = fp.readline()
        # Once all lines are read this just returns ''
        # until the file changes and a new line appears
        if not go and stop in new:
            go = True
            print('turn on')
        if go:
            for word in words.keys():
                if word in new:
                    go = False
                    yield word, words[word]


def get_pid(pname='googlesamples-assistant-pushtotalk'):
    p = subprocess.check_output(['ps', '-C', pname, '-o', 'pid='])
    p = p.decode('utf-8')
    p = int(p)
    return p
    

def get_sink():
    p = get_pid()
    o = subprocess.check_output(['pacmd', 'list-sink-inputs'])
    o = o.decode('utf-8')
    can = re.findall(r'index: (\d+)', o)
    idx = re.findall(r'application.process.id = [\S ]+', o)
    index = idx.index('application.process.id = "{0}"'.format(p))
    return can[index]


def execute():
    command = './start_sample.sh'
    command_line = shlex.split(command)
    subprocess.Popen(command_line, shell=True)
    
    print('Wait for execute G.A.')
    time.sleep(1)


def mute():
    idx = get_sink()
    print('Mute', idx)
    subprocess.run(['pacmd', 'set-sink-input-mute', idx, 'true'])


def unmute():
    idx = get_sink()
    print('Unmute', idx)
    subprocess.run(['pacmd', 'set-sink-input-mute', idx, 'false'])


def kill():
    command = 'killall start_sample.sh'
    command_line = shlex.split(command)
    subprocess.run(command_line)
    command = 'killall googlesamples-assistant-pushtotalk'
    command_line = shlex.split(command)
    subprocess.run(command_line)


def control_hue(on):
    for light in b.lights:
        light.on = on


fn = 'out'
words = {'"how\'s the weather".': (subprocess.run, ['mpv', '--loop-playlist=no', 
                                      '--keep-open=no', 'weather.mp3']),
         '"play music".': (subprocess.run, ['mpv', '--loop-playlist=no', 
                                      '--keep-open=no', 'music.mp4']),
         '"news".': (subprocess.run, ['mpv', '--loop-playlist=no', 
                                      '--keep-open=no', 'news.mp4']),
         '"what time is it".': (play_time, None),
         '"turn lights on".': (control_hue, True),
         '"turn off lights".': (control_hue, False),
         }
stop = 'Recording audio request.'
subprocess.run(['rm', fn])
subprocess.run(['touch', fn])
execute()
for intent, command in watch(fn, words, stop):
    print('Detected: ', intent)
    mute()
    command[0](command[1])
    print('sleep 1')
    time.sleep(1)
    unmute()

