import os
import sys
import shutil
import csv
import subprocess
import datetime
import xml.etree.ElementTree as ET
import random
import re
import time


def setup_android(path):
    command = 'adb shell su -c cp {0} /sbin/tcpdump'.format(path)
    command_check(command)
    command = 'adb shell su -c chmod +x /sbin/tcpdump'
    command_check(command)


def check_binary(binaries):
    for binary in binaries:
        if shutil.which(binary) is None:
            raise FileNotFoundError


def check_dirs(dirs):
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)


def clear_env(pss):
    for ps in pss:
        command = 'adb shell "ps | grep {0}"'.format(ps)
        try:
            output = command_output(command)
        except subprocess.CalledProcessError:
            continue
        psnum = re.findall('\d+', output)[0]
        command = 'adb shell su -c kill -9 {0}'.format(psnum)
        command_check(command)


def terminate_env(pss):
    for ps in pss:
        command = 'adb shell "ps | grep {0}"'.format(ps)
        try:
            output = command_output(command)
        except subprocess.CalledProcessError:
            continue
        psnum = re.findall('\d+', output)[0]
        command = 'adb shell su -c kill -2 {0}'.format(psnum)
        command_check(command)


def command_popen(command):
    return subprocess.Popen(command, shell=True)


def command_check(command):
    return subprocess.check_call(command, shell=True)


def command_output(command):
    return subprocess.check_output(command, shell=True).decode('utf-8')


def write_relative_timing(start_time):
    pass


def send_ping():
    command = 'adb shell su -c ping -c 1 -w 1 -I wlan0 127.0.0.1'
    return command_popen(command)


def terminate_ping(ping_proc):
    try:
        ping_proc.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        ping_proc.kill()
        ping_proc.communicate()


def get_second_from_start(start_time):
    return abs(int((start_time - datetime.datetime.now()).total_seconds()))


def parse_xml_log(path):
    tree = ET.parse(path)
    root = tree.getroot()
    it = root.iter()
    size = 0
    bounds = list()
    for item in it:
        size = size+1
        if item.get('clickable') == 'true':
            bounds.append(item.get('bounds'))

    try:
        choose = random.choice(bounds)
        axes = re.findall('\d+', choose)
        point = (random.randrange(int(axes[0]), int(axes[2])),
                 random.randrange(int(axes[1]), int(axes[3])))
    except ValueError:
        point = (random.randrange(0, 1080),
                 random.randrange(0, 1920))
    except IndexError:
        point = (random.randrange(0, 1080),
                 random.randrange(0, 1920))
    return size, point


def main(argv=sys.argv):
    if len(argv) < 1:
        print('Can not reached line')
        os.exit(0)
    # Check binaries
    binaries = ['adb']
    check_binary(binaries)
    # Check dirs
    dirs = ['./output/mp4']
    check_dirs(dirs)
    # Clear env
    print('checked all binaries, dirs')

    # Get list of target apps
    if not os.path.exists('app_list.csv'):
        raise Exception('Need app_list.csv')
    app_list = list()
    with open('app_list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['package_name'])
            app_list.append(row['package_name'])
    # package_name = app_list[0]

    for package_name in app_list:
        pss = ['screenrecord']
        clear_env(pss)
        # clear cache without user data
        # adb shell pm clear APKNAME
        # adb shell run-as APKNAME rm -rf /data/data/APKNAME/cache/*
        # adb shell su - c rm - rf /data/data/com.amazon.mShop.android.shopping/cache/*
        command = 'adb shell su -c rm -rf /data/data/{0}/cache/*'.format(package_name)
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        command = 'adb shell su -c rm /sdcard/*.xml'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        command = 'adb shell su -c rm /sdcard/*.mp4'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        command = 'adb shell su -c rm /sdcard/*.pcap'
        try:
            command_check(command)
        except subprocess.CalledProcessError:
            pass
        print('removed cache')

        # time_list
        timing_list = list()

        # execute screenrecord
        command = 'adb shell screenrecord /sdcard/{0}.mp4'.format(package_name)
        screenrecord_proc = command_popen(command)

        # launch app
        start_time = datetime.datetime.now()
        command = 'adb shell monkey -p {0} -c android.intent.category.LAUNCHER 1'.format(package_name)
        command_check(command)

        # sleep
        time.sleep(10)

        # stop app
        for index in range(0, 1):
            command = 'adb shell input keyevent KEYCODE_HOME'
            command_check(command)

        command = 'adb shell monkey -p {0} -c android.intent.category.LAUNCHER 1'.format(package_name)
        command_check(command)

        # sleep
        time.sleep(10)

        # stop app
        for index in range(0, 5):
            command = 'adb shell input keyevent KEYCODE_BACK'
            command_check(command)

        command = 'adb shell monkey -p {0} -c android.intent.category.LAUNCHER 1'.format(package_name)
        command_check(command)

        # sleep
        time.sleep(10)

        command = 'adb shell am force-stop {0}'.format(package_name)
        command_check(command)

        # terminate screenrecord
        screenrecord_proc.terminate()
        screenrecord_proc.kill()

        # why?
        pss = ['screenrecord']
        terminate_env(pss)

        time.sleep(5)

        # pull mp4
        command = 'adb pull /sdcard/{0}.mp4 ./output/mp4/'.format(package_name)
        command_check(command)


if __name__ == '__main__':
    main()
