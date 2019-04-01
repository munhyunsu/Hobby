import socket


def main()
    ssocket = socket.socket(socket.AF_INET,
                            socket.SOCK_STREAM)

    host = socket.gethostname(FLAGS.host_name)
    port = int(FLAGS.port)

    ssocket.bind((host, port))

    ssocket.listen(5)

    try:
        print('Executed server')
        while True:
            csocket, caddr = ssocket.accept()
            print('Got a connection from {0}'.format(caddr))

            msg = 'Thank you for connecting'
            csocket.send(msg.encode('utf-8'))
            csocket.close()
    except KeyboardInterrupt:
        print('Terminated server')

