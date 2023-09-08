import os
import sys
import math
import wave
import struct
import statistics

import morsecode

FLAGS = _ = None
DEBUG = False
INTMAX = 2**(32-1)-1
THRESHOLD = 10000


def file2morse(filename):
    t = FLAGS.timing
    fs = FLAGS.samplerate
    with wave.open(filename, 'rb') as w:
        audio = []
        framerate = w.getframerate()
        frames = w.getnframes()
        for i in range(frames):
            frame = w.readframes(1)
            audio.append(struct.unpack('<i', frame)[0])
        morse = ''
        unit = int(t * fs)
        for i in range(1, math.ceil(len(audio)/unit)+1):
            stdev = statistics.stdev(audio[(i-1)*unit:i*unit])
            if stdev > THRESHOLD:
                morse = morse + '.'
            else:
                morse = morse + ' '
        morse = morse.replace('...', '-')
        morse = morse.replace('       ', 'm')
        morse = morse.replace('   ', 's')
        morse = morse.replace(' ', '')
        morse = morse.replace('s', ' ')
        morse = morse.replace('m', ' / ')
        morse = morse
    return morse

def morse2text(morse):
    text = ''
    for code in morse.split(' '):
        if code == '/':
            text = text + ' '
        for key, value in morsecode.english.items():
            if code == value:
                text = text + key
        for key, value in morsecode.number.items():
            if code == value:
                text = text + key
    return text


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')
    print(f'Input wav: {FLAGS.input}')
    morse = file2morse(FLAGS.input)
    print(f'Morse code: {morse}')
    text = morse2text(morse)
    print(f'Text: {text}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                         help='The present debug message')
    parser.add_argument('--timing', default=0.1, type=int,
                         help='The unit of message time')
    parser.add_argument('--samplerate', default=48000, type=int,
                         help='The WAV sample rate')
    parser.add_argument('--frequency', default=523.251, type=float,
                         help='The frequency of WAV file')
    parser.add_argument('--input', required=True, type=str,
                         help='The input wav')


    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))

    main()

