import os
import sys
from scapy.all import *

ARGS = None


def pkt_writer(pkts):
    wrpcap(ARGS.output, pkts, append=True)

def main():
    if os.path.exists(ARGS.output):
        prompt = ('{0} file exists, '
                  '\x1B[1mdelete\x1B[0m it?(Y/N) ').format(ARGS.output)
        user_input = input(prompt)
        if user_input.lower() == 'y':
            print('Delete {0}'.format(ARGS.output))
            os.remove(ARGS.output)
        else:
            print('Append {0}'.format(ARGS.output))
    try:
        print('Start sniff')
        sniff(prn=pkt_writer, filter=ARGS.filter)
    except KeyboardInterrupt:
        pass
    pkts = rdpcap(ARGS.output)
    print('Terminate sniffing')
    print(repr(pkts))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', type=str, 
                        default='', help='BPF')
    parser.add_argument('-o', '--output', type=str, 
                        default='./output.pcap', help='output file path')

    ARGS = parser.parse_args()
    ARGS.output = os.path.abspath(os.path.expanduser(ARGS.output))

    main()

