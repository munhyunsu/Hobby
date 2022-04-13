import threading
import socketserver
import itertools

FLAGS = _ = None
DEBUG = False

lock = threading.Lock()
storage = []


def do_full_league(pools, rounds):
    for p1, p2 in itertools.combinations(pools, 2):
        if DEBUG:
            print(f'{p1.name} vs {p2.name}')
        for r, h1, h2 in zip(range(1, rounds+1),
                             itertools.cycle(p1.hands),
                             itertools.cycle(p2.hands)):
            print(f'{r} {h1} {h2}')


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
            lock.acquire()
            storage.append(process_message(message))
            lock.release()
            data = f'Ok'.encode('utf-8')
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

    do_full_league(storage, FLAGS.rounds)


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
    parser.add_argument('--rounds', type=int, default=10,
                        help='The rounds')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

