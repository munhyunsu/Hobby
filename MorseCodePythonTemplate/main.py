import os
import sys
import re
import math
import wave
import struct
import statistics
import time

import pyaudio

import morsecode

FLAGS = _ = None
DEBUG = False
CHANNELS = 1
SAMPLERATE = 48000
FREQUENCY = 523.251
UNIT = 0.1
SHORTMAX = 2**(16-1)-1
MORSE_THRESHOLD = SHORTMAX // 4
UNSEEN_THRESHOLD = 3.0


def text2morse(text):
    text = text.upper()
# Need to edit below!
    morse = '-.-. ... .'
# Need to edit above!

    return morse


def morse2audio(morse):
    audio = []
# Need to edit below!
    for m in morse:
        if m == '.':
            for i in range(math.ceil(SAMPLERATE*UNIT)*1):
                audio.append(int(SHORTMAX*math.sin(2*math.pi*FREQUENCY*i/SAMPLERATE)))
        elif m == '-':
            for i in range(math.ceil(SAMPLERATE*UNIT)*3):
                audio.append(int(SHORTMAX*math.sin(2*math.pi*FREQUENCY*i/SAMPLERATE)))
        for i in range(math.ceil(SAMPLERATE*UNIT)*1):
            audio.append(int(0))
# Need to edit above!
    return audio


def play_audio(audio):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLERATE,
                    frames_per_buffer=SAMPLERATE,
                    output=True)

    for a in audio:
        stream.write(struct.pack('<h', a))

    time.sleep(0.5/UNIT) # Wait for play

    stream.stop_stream()
    stream.close()
    p.terminate()


def send_data():
    while True:
        print('Type some text (only English)')
        text = input('User input: ').strip()
        if re.match(r'[A-Za-z0-9 ]+', text):
            break
    morse = text2morse(text)
    print(f'MorseCode: {morse}')
    audio = morse2audio(morse)
    print(f'AudioSize: {len(audio)}')
    play_audio(audio)


def record_audio():
    unit_size = math.ceil(SAMPLERATE*UNIT)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=SAMPLERATE,
                    frames_per_buffer=SAMPLERATE,
                    input=True)

# Need to edit below!
    morse = ''
    while True:
        data = stream.read(unit_size)
        for i in range(0, len(data), 2):
            d = struct.unpack('<h', data[i:i+2])[0]
            if abs(d) > MORSE_THRESHOLD:
                morse = '-.-. ... .'
                break
        if len(morse) != 0:
            print(f'RawMorse: {morse}')
            stream.stop_stream()
            stream.close()
            p.terminate()
            break
# Need to edit above!

    return morse


def morse2text(morse):
    text = ''
# Need to edit below!
    text = text + 'CSE'
# Need to edit above!
    return text


def receive_data():
    morse = record_audio()
    print(f'Morse: {morse}')
    text = morse2text(morse)
    print(f'Sound input: {text}')


def main():
    while True:
        print('Morse Code Data Communication 2022')
        print('[1] Send data over sound (play)')
        print('[2] Receive data over sound (record)')
        print('[q] Exit')
        select = input('Select menu: ').strip().upper()
        if select == '1':
            send_data()
        elif select == '2':
            receive_data()
        elif select == 'Q':
            print('Terminating...')
            break;


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                         help='The present debug message')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

