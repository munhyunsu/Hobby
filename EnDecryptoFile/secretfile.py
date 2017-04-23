#!/usr/bin/env python3

import sys
import getpass
from Crypto.Cipher import DES
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Util import Counter
import Crypto.Util

def encrypto_file(target_file):
    print('암호화를 시작합니다.')
    print('암호화 알고리즘을 선택하세요.')
    print('[1] DES')
    print('[2] AES')
    print('[DEFAULT] AES')
    user_input = input('입력: ')
    try:
        user_input = int(user_input)
    except:
        print('기본값을 사용합니다.')
        user_input = 2
    if user_input == 1:
        algorithm = 'DES'
    elif user_input == 2:
        algorithm = 'AES'
    else:
        print('[FATAL] 알 수 없는 오류 발생')
        sys.exit(1)
    print('')
    print('블록암호 운용방식을 선택하세요.')
    print('[1] CTR')
    print('[2] CBC')
    print('[DEFAULT] CBC')
    user_input = input('입력: ')
    try:
        user_input = int(user_input)
    except:
        print('기본값을 사용합니다.')
        user_input = 2
    if user_input == 1:
        mode = 'CTR'
    elif user_input == 2:
        mode = 'CBC'
    else:
        print('[FATAL] 알 수 없는 오류 발생')
        sys.exit(1)
    print('')
    print('암호화 키를 입력하세요.')
    while True:
        user_input = getpass.getpass('패스워드 입력: ')
        try:
            password = user_input.encode('ascii')
            hasing = SHA256.new()
            hasing.update(password)
            password = hasing.digest()
            break
        except UnicodeEncodeError:
            print('아스키코드 변환중 오류가 발생했습니다.')
            print('아스키코드에 있는 문자로 입력해주세요.')
    print('')
    if algorithm == 'DES':
        if mode == 'CTR':
            enc_des_ctr(target_file, password[:8])
        elif mode == 'CBC':
            enc_des_cbc(target_file, password[:8])
        else:
            print('[FATAL] 알 수 없는 오류 발생!')
            sys.exit(1)
    elif algorithm == 'AES':
        if mode == 'CTR':
            enc_aes_ctr(target_file, password)
        elif mode == 'CBC':
            enc_aes_cbc(target_file, password)
        else:
            print('[FATAL] 알 수 없는 오류 발생!')
            sys.exit(1)
    print('암호화 완료!')


def enc_aes_ctr(target_file, password):
    ctr = Crypto.Util.Counter.new(AES.block_size*8)
    cipher = AES.new(password, AES.MODE_CTR, counter = ctr)
    with open(target_file, 'rb') as src:
        o_msg = src.read()
        o_msg = msg_pad(o_msg, DES.block_size)
        e_msg = b'\x04' + cipher.encrypt(o_msg)
        with open(target_file + '_enc', 'wb') as dst:
            dst.write(e_msg)


def enc_aes_cbc(target_file, password):
    iv = b'\x00'*16
    cipher = AES.new(password, AES.MODE_CBC, IV = iv)
    with open(target_file, 'rb') as src:
        o_msg = src.read()
        o_msg = msg_pad(o_msg, AES.block_size)
        e_msg = b'\x03' + cipher.encrypt(o_msg)
        with open(target_file + '_enc', 'wb') as dst:
            dst.write(e_msg)


def enc_des_ctr(target_file, password):
    ctr = Crypto.Util.Counter.new(DES.block_size*8)
    cipher = DES.new(password, DES.MODE_CTR, counter = ctr)
    with open(target_file, 'rb') as src:
        o_msg = src.read()
        o_msg = msg_pad(o_msg, DES.block_size)
        e_msg = b'\x02' + cipher.encrypt(o_msg)
        with open(target_file + '_enc', 'wb') as dst:
            dst.write(e_msg)

def enc_des_cbc(target_file, password):
    iv = b'\x00'*8
    cipher = DES.new(password, DES.MODE_CBC, iv)
    with open(target_file, 'rb') as src:
        o_msg = src.read()
        o_msg = msg_pad(o_msg, DES.block_size)
        e_msg = b'\x01' + cipher.encrypt(o_msg)
        with open(target_file + '_enc', 'wb') as dst:
            dst.write(e_msg)


def msg_pad(msg, block_size):
    return msg + (b' ' * (block_size-(len(msg)%block_size)))


def decrypto_file(target_file):
    """
    """
    print('암호화 키를 입력하세요.')
    while True:
        user_input = getpass.getpass('패스워드 입력: ')
        try:
            password = user_input.encode('ascii')
            hasing = SHA256.new()
            hasing.update(password)
            password = hasing.digest()
            break
        except UnicodeEncodeError:
            print('아스키코드 변환중 오류가 발생했습니다.')
            print('아스키코드에 있는 문자로 입력해주세요.')
    print('')
    with open(target_file, 'rb') as src:
        e_msg = src.read()
        enc_mode = e_msg[0]
        if enc_mode == 1:
            dec_des_cbc(target_file, password[:8])
        elif enc_mode == 2:
            dec_des_ctr(target_file, password[:8])
        elif enc_mode == 3:
            dec_aes_cbc(target_file, password)
        elif enc_mode == 4:
            dec_aes_ctr(target_file, password)
        else:
            print('[FATAL] 암호 파일이 잘 못 된 것 같습니다.')
            sys.exit(1)
    print('복호화 완료')


def dec_aes_ctr(target_file, password):
    ctr = Crypto.Util.Counter.new(AES.block_size*8)
    cipher = AES.new(password, AES.MODE_CTR, counter = ctr)
    with open(target_file, 'rb') as src:
        e_msg = src.read()[1:]
        d_msg = cipher.decrypt(e_msg)
        with open(target_file[:-4] + '_dec', 'wb') as dst:
            dst.write(d_msg)


def dec_aes_cbc(target_file, password):
    iv = b'\x00'*16
    cipher = AES.new(password, AES.MODE_CBC, iv)
    with open(target_file, 'rb') as src:
        e_msg = src.read()[1:]
        d_msg = cipher.decrypt(e_msg)
        with open(target_file[:-4] + '_dec', 'wb') as dst:
            dst.write(d_msg)


def dec_des_ctr(target_file, password):
    ctr = Crypto.Util.Counter.new(DES.block_size*8)
    cipher = DES.new(password, DES.MODE_CTR, counter = ctr)
    with open(target_file, 'rb') as src:
        e_msg = src.read()[1:]
        d_msg = cipher.decrypt(e_msg)
        with open(target_file[:-4] + '_dec', 'wb') as dst:
            dst.write(d_msg)
    

def dec_des_cbc(target_file, password):
    iv = b'\x00'*8
    cipher = DES.new(password, DES.MODE_CBC, iv)
    with open(target_file, 'rb') as src:
        e_msg = src.read()[1:]
        d_msg = cipher.decrypt(e_msg)
        with open(target_file[:-4] + '_dec', 'wb') as dst:
            dst.write(d_msg)


def main(argv):
    if len(argv) < 2:
        print('대상 파일을 인자로 넣어주세요.')
        sys.exit(0)
    target_file = argv[1]
    print('안녕하세요. 관용암호 방식의 암호화 프로그램입니다.')
    print('입력 파일인 {}을 암/복호화 합니다.'.format(target_file))
    print('')
    print('암/복호화를 선택하세요.')
    print('[1] 암호화')
    print('[2] 복호화')
    default_input = 1
    if target_file[-4:] == '_enc':
        print('파일명으로 유추하면 복호화를 해야합니다.')
        default_input = 2
    print('[DEFAULT] {}'.format(default_input))
    user_input = input('입력: ')
    try:
        user_input = int(user_input)
    except:
        print('기본값을 사용합니다.')
        user_input = default_input
    
    if user_input == 1:
        encrypto_file(target_file)
    elif user_input == 2:
        decrypto_file(target_file)
    else:
        print('[FATAL] 알 수 없는 오류 발생!')
        

if __name__ == '__main__':
    sys.exit(main(sys.argv))
