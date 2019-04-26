import subprocess
import shlex
import time
import datetime
import re
import csv

FLAGS = None


def get_cwnd(target):
    result = list()
    lines = target.split('\n')[1:]
    for index in range(0, len(lines), 2):
        try:
            header = lines[index].strip()
            body = lines[index+1].strip()
        except IndexError:
            break
        send_q = int(re.findall(r'\S+', header)[3])
        peer = re.findall(r'\S+', header)[5]
        alg = re.findall(r'\S+', body)[0]
        cwnd = re.findall(r'(?<=cwnd:)\d+', body)[0]
        result.append((peer, alg, cwnd))
    return result

def write_csv(result, port):
    fieldnames = ['mtime', 'peer', 'alg', 'cwnd']
    with open(FLAGS.output, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        base_time = result[0]['mtime']
        for row in result:
            #if int(row['peer'].split(':')[-1]) == port:
            if row['peer'].endswith(port):
                row['mtime'] = row['mtime'] - base_time
                writer.writerow(row)

def main(_):
    print(FLAGS, _)
    start_time = time.time()
    current_time = time.time()
    mtime = current_time-start_time
    result = list()

    print('Start measurement during {0} seconds'.format(FLAGS.time))

    while mtime < FLAGS.time:
        current_time = time.time()
        mtime = current_time-start_time
        command_line = 'ss -i sport = :{0}'.format(FLAGS.port)
        command = shlex.split(command_line)
        process = subprocess.run(command, stdout=subprocess.PIPE, timeout=1)
        output = process.stdout.decode('utf-8')
        cwnd_result = get_cwnd(output)
        for peer, alg, cwnd in cwnd_result:
            result.append({'mtime': mtime,
                           'alg': alg,
                           'peer': peer,
                           'cwnd': cwnd})
        time.sleep(FLAGS.sleep)

    target_port = input('Input target port number: ')

    write_csv(result, target_port)
    print('Measurement ended')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time', type=int, default=15,
                        help='Measurement time')
    parser.add_argument('-p', '--port', type=int, required=True,
                        help='Measurement port')
    parser.add_argument('-s', '--sleep', type=int, default=0,
                        help='Sleep time')
    parser.add_argument('-o', '--output', type=str, default='output.csv',
                        help='Output csv file path')

    FLAGS, _ = parser.parse_known_args()

    main(_)

