import socket
import ssl
import threading

FLAGS = None


def worker(csock, caddr):
    try:
        #print('Connected with {0}'.format(caddr))
        cdata = csock.recv(1500).decode('utf-8')
        cmethod, cpath, cproto = (cdata.split('\r\n')[0]).split(' ')
        if cpath == '/':
            cpath = '/index'
        if '.' not in cpath:
            cpath = '{0}.html'.format(cpath)
        path = '.{0}'.format(cpath)
        with open(path, 'r') as f:
            content = f.read()
        sdata = ('HTTP/1.1 200 OK\r\n'
                 'Content-Type: text/html; encoding=utf8\r\n'
                 'Content-Length: {0}\r\n'
                 'Connection: close\r\n'
                 '\r\n'
                 '{1}').format(len(content), content).encode('utf-8')
        csock.sendall(sdata)
    except FileNotFoundError:
        sdata = ('HTTP/1.1 404 Not Found\r\n'
                 'Content-Type: text/html; encoding=utf8\r\n'
                 'Content-Length: 2\r\n'
                 'Connection: close\r\n'
                 '\r\n'
                 'No').encode('utf-8')
        csock.sendall(sdata)
    csock.close()


def main(_):
    print('Parsed args {0}'.format(FLAGS))
    print('Unparsed args {0}'.format(_))

    # Create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse
    sock.bind(('', FLAGS.port))
    sock.listen()

    # Wrap-up secure socket
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(FLAGS.cert, FLAGS.key)
    ssock = context.wrap_socket(sock, server_side=True)

    print('Start server')
    while True:
        try:
            csock, caddr = ssock.accept()
            thread = threading.Thread(target=worker,
                                      args=(csock, caddr))
            thread.start()
            print('Start process {0}'.format(thread))
        except KeyboardInterrupt:
            print('End server')
            for thread in threading.enumerate():
                if thread.getName() == 'MainThread':
                    continue
                print('Join thread {0}'.format(thread))
                thread.join(timeout=1)
            break
        except ssl.SSLError:
            pass
        except ConnectionResetError:
            pass


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        help='Server port number')
    parser.add_argument('-c', '--cert',
                        required=True,
                        help='Server certificate file path')
    parser.add_argument('-k', '--key',
                        required=True,
                        help='Server key file path')

    FLAGS, _ = parser.parse_known_args()
    
    main(_)

