from scapy.all import *
import os
import socket

FLAGS = None


def main(_):
    syn = IP(dst=FLAGS.ip)/TCP(sport=os.getpid(), dport=FLAGS.port, flags='S')
    input('Send? {0}'.format(repr(syn)))
    syn_ack = sr1(syn)
    print('Received {0}'.format(repr(syn_ack)))
    ack = IP(dst=FLAGS.ip)/TCP(sport=syn_ack[TCP].dport, dport=FLAGS.port, 
                               seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq+1, 
                               flags='A')
    input('Send? {0}'.format(repr(ack)))
    send(ack)


if __name__ == '__main__':
    import argparse

    # http://www.secdev.org/projects/scapy/doc/troubleshooting.html
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--iface', type=str,
                        default='wlp2s0')
    parser.add_argument('-i', '--ip', type=str,
                        default='localhost')
    parser.add_argument('-p', '--port', type=int,
                        default=6292)

    FLAGS, _ = parser.parse_known_args()

    # http://www.secdev.org/projects/scapy/doc/troubleshooting.html
    if FLAGS.iface == 'lo':
        print('changed conf.L3socket')
        conf.L3socket=L3RawSocket
    main(_)

