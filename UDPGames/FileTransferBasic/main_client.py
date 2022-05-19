import socket

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'Ready to send using {sock}')

    while True:
        try:
            filename = input('Filename: ').strip()
            request = f'INFO {filename}'
            sock.sendto(request.encode('utf-8'), (FLAGS.address, FLAGS.port))

            response, server = sock.recvfrom(FLAGS.chunk_maxsize)
            response = response.decode('utf-8')
            if response == '404 Not Found':
                print(response)
                continue
            size = int(response)

            request = f'DOWNLOAD {filename}'
            sock.sendto(request.encode('utf-8'), (FLAGS.address, FLAGS.port))
            print(f'Request {filename} to ({FLAGS.address}, {FLAGS.port})')

            remain = size
            with open(filename, 'wb') as f:
                while remain > 0:
                    chunk, server = sock.recvfrom(FLAGS.chunk_maxsize)
                    chunk_size = len(chunk)
                    if chunk_size == 0:
                        break
                    remain = remain - chunk_size
                    f.write(chunk)
                    if DEBUG:
                        print(f'Receiving from {server}: {size-remain}/{size}')
            print(f'File download success')
        except KeyboardInterrupt:
            print(f'Shutting down... {sock}')
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='localhost',
                        help='The address to send data')
    parser.add_argument('--port', type=int, default=38442,
                        help='The poort to send data')
    parser.add_argument('--chunk_maxsize', type=int, default=2**16,
                        help='The recvfrom chunk max size')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

