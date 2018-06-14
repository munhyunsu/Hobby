import sys
import socket

HOST = ''
PORT = 12345
ADDR = (HOST, PORT)
BUFSIZE = 4096
FILENAME = 'server_recv'

def main(argv = sys.argv):
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serv.bind(ADDR)
    serv.listen(1)

    print('Listening ...')

    while True:
        conn, addr = serv.accept()
        print('Client connected ... {0}'.format(addr))
        myfile = open(FILENAME, 'wb')

        cnt = 0
        while True:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            myfile.write(data)
            cnt = cnt+1
            print('Writing file .... {0}'.format(cnt))
        
        print('Completed ... {0}'.format(addr))
        
    myfile.close()
    print('Finished writing file')
    conn.close()
    print('Client disconnected')


if __name__ == '__main__':
    sys.exit(main())
