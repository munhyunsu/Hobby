import os
import threading
import socketserver
import itertools
import operator
import csv

FLAGS = _ = None
DEBUG = False

lock = threading.Lock()
storage = []
verifier = set()

def do_full_league(pools, rounds):
    result = {}
    for p1, p2 in itertools.combinations(pools, 2):
        if DEBUG:
            print(f'{p1.name} vs {p2.name}')
        s1 = 0
        s2 = 0
        for r, h1, h2 in zip(range(1, rounds+1),
                             itertools.cycle(p1.hands),
                             itertools.cycle(p2.hands)):
            if h1 == 'kawi' and h2 == 'kawi':
                pass
            elif h1 == 'kawi' and h2 == 'bawi':
                s2 = s2 + 1
            elif h1 == 'kawi' and h2 == 'bo':
                s1 = s1 + 1
            elif h1 == 'bawi' and h2 == 'kawi':
                s1 = s1 + 1
            elif h1 == 'bawi' and h2 == 'bawi':
                pass
            elif h1 == 'bawi' and h2 == 'bo':
                s2 = s2 + 1
            elif h1 == 'bo' and h2 == 'kawi':
                s2 = s2 + 1
            elif h1 == 'bo' and h2 == 'bawi':
                s1 = s1 + 1
            elif h1 == 'bo' and h2 == 'bo':
                pass
        if s1 > s2:
            result[p1] = result.get(p1, 0) + 3
            result[p2] = result.get(p2, 0) - 1
        elif s1 < s2:
            result[p1] = result.get(p1, 0) - 1
            result[p2] = result.get(p2, 0) + 3
        else:
            result[p1] = result.get(p1, 0) + 1
            result[p2] = result.get(p2, 0) + 1
    return result


class Player():
    def __init__(self, name, hands):
        self.name = name
        self.hands = hands

    def __repr__(self):
        return f'{self.name} {self.hands}'


def process_message(message):
    tokens = message.split(' ')
    name = tokens[0]
    hands = []
    for token in tokens[1:]:
        token = token.lower()
        if token not in ('kawi', 'bawi', 'bo'):
            raise Exception
        hands.append(token)
    player = Player(name, hands)
    return player


class ThreadedUDPRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        message = self.rfile.read().decode('utf-8')
        if DEBUG:
            print(f'{message} from {self.client_address}')
        try:
            card = process_message(message)
            if len(verifier) == 0 or card.name in verifier:
                print(f'Join {card.name}')
                lock.acquire()
                storage.append(card)
                lock.release()
                data = f'Ok'.encode('utf-8')
                self.wfile.write(data)
            else:
                print(f'Failed {card.name}')
                data = f'Not verified'.encode('utf-8')
                self.wfile.write(data)
        except:
            data = f'Error'.encode('utf-8')
            self.wfile.write(data)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    if FLAGS.verify is not None:
        with open(FLAGS.verify, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                verifier.add(row[0])
    if DEBUG:
        print(f'{verifier=}')

    server = ThreadedUDPServer((FLAGS.address, FLAGS.port),
                               ThreadedUDPRequestHandler)
    server.allow_reuse_address = True

    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        try:
            server_thread.start()
            server_thread.join()
        except KeyboardInterrupt:
            server.shutdown()

    if DEBUG:
        print('Players')
        for item in storage:
            print(item)

    pools = []
    for player in storage:
        pools.append(player)
    while True:
        result = do_full_league(pools, FLAGS.rounds)
        sorted_result = sorted(result.items(),
                               key=operator.itemgetter(1),
                               reverse=True)
        if FLAGS.show:
            print(f'Scoreboard with {len(result)} players')
            for idx, item in enumerate(sorted_result, start=1):
                print(f'[{idx:>2d}] {item[0].name:>10s} {item[1]:>3d}')
            print(f'Press enter', end='')
            input()
        if len(result) <= FLAGS.final:
            break
        pools.clear()
        for i in range(len(result)//2):
            pools.append(sorted_result[i][0])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='localhost',
                        help='The address to serve service')
    parser.add_argument('--port', type=int, default=6292+2022,
                        help='The poort to serve service')
    parser.add_argument('--final', type=int, default=4,
                        help='The final players')
    parser.add_argument('--rounds', type=int, default=100,
                        help='The rounds')
    parser.add_argument('--show', action='store_true',
                        help='The break show per split')
    parser.add_argument('--verify', type=str,
                        help='The player verifing data')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    if FLAGS.verify is not None:
        FLAGS.verify = os.path.abspath(os.path.expanduser(FLAGS.verify))

    main()

