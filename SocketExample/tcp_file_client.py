import sys
import socket

HOST = 'localhost'
PORT = 12345
ADDR = (HOST, PORT)
FILENAME = 'client_recv'

def main(argv = sys.argv):
    
    myfile = open(argv[1], 'rb').read()
    print('Readed ... {0}'.format(len(myfile)))

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    client.send(myfile)
    print('Sended ...')

    client.close()


if __name__ == '__main__':
    sys.exit(main())
