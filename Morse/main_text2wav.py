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


def get_signal(exp):
    t = FLAGS.timing*exp
    fs = FLAGS.samplerate
    f = FLAGS.frequency
    audio = []
    for i in range(int(t*fs)):
        audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))
    return audio


def get_silence(exp):
    t = FLAGS.timing*exp
    fs = FLAGS.samplerate
    f = FLAGS.frequency
    audio = []
    for i in range(int(t*fs)):
        audio.append(int(0))
    return audio


def text2morse(text):
    text = text.upper()
    morse = ''

    for t in text:
        if t == ' ':
            morse = morse + '/'
        for key, value in morsecode.english.items():
            if t == key:
                morse = morse + value
        for key, value in morsecode.number.items():
            if t == key:
                morse = morse + value
        morse = morse + ' '

    return morse[:-1]


def morse2audio(morse):
    audio = []
    for m in morse:
        if m == '.':
            audio.extend(get_signal(exp=1))
        elif m == '-':
            audio.extend(get_signal(exp=3))
        elif m == ' ':
            audio.extend(get_silence(exp=1))
        elif m == '/':
            audio.extend(get_silence(exp=1))
        audio.extend(get_silence(exp=1))
    return audio


def audio2file(audio, filename):
    fs = FLAGS.samplerate
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(4)
        w.setframerate(fs)
        for a in audio:
            w.writeframes(struct.pack('<l', a))


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')
    print(f'Input text: {FLAGS.text}')
    morse = text2morse(FLAGS.text)
    print(f'Morse code: {morse}')
    audio = morse2audio(morse)
    audio2file(audio, FLAGS.output)
    print(f'Morse code WAV file created: {FLAGS.output}')


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
    parser.add_argument('--text', required=True, type=str,
                         help='The input text')
    parser.add_argument('--output', default='output.wav', type=str,
                         help='The output path')


    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))

    main()

