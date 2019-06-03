/*
  Socket example: server
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

// http://man7.org/linux/man-pages/man2/listen.2.html
#define MAXBACKLOG 5
#define BUFFSIZE 1500

int main(int argc, char* argv[]) {
    /* prepare local variables */
    int sock_server, sock_client; // Socket descriptor
    struct sockaddr_in addr_server, addr_client; // Addresses
    unsigned short port_server; // Port number of server
    unsigned int client_addr_len; // client address structure
    int readlen; // readed buf length
    char buf[BUFFSIZE]; // read buffer

    /* arguments parsing */
    if(argc != 2) { // check server port as arguments
        printf("Usage: a.out [SERVERPORT]\n");
        exit(1);
    }
    port_server = atoi(argv[1]); // port number

    /* create socket */
    if( (sock_server = /* NEEDFIX: socket create */socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        printf("socket() error\n");
        exit(1);
    }

    /* server address structing */
    memset(&addr_server, 0, sizeof(addr_server)); // zero set
    addr_server.sin_family = AF_INET; // Internet address family
    addr_server.sin_addr.s_addr = htonl(INADDR_ANY); // any interface
    addr_server.sin_port = htons(port_server); // port number

    /* bind socket to address and port */
    if( /* NEEDFIX: bind socket */bind(sock_server, (struct sockaddr *) &addr_server, 
            sizeof(addr_server)) < 0) {
        printf("bind() error\n");
        exit(1);
    }

    /* listen connection */
    if( /* NEEDFIX: listen */listen(sock_server, MAXBACKLOG) < 0) {
        printf("listen() error\n");
        exit(1);
    }

    /* client accept */
    while(1) {
        /* create client socket */
        client_addr_len = sizeof(addr_client);
        if( (sock_client = /*NEEDFIX: accept */ accept(sock_server, 
                                  (struct sockaddr *) &addr_client,
                                  &client_addr_len)) < 0) {
            printf("accept() error\n");
            exit(1);
        }

        /* serve client */
        printf("Connected %s\n", inet_ntoa(addr_client.sin_addr));
        while(1) {
            if( (readlen = /* NEEDFIX: recv echo string */recv(sock_client, buf, BUFFSIZE, 0)) < 0) {
                printf("recv() error\n");
                exit(1);
            }
            if(readlen > 0) {
                if( /*NEEDFIX: send string */send(sock_client, buf, readlen, 0) != readlen ) {
                    printf("send() error\n");
                    exit(1);
                }
                buf[readlen] = '\0';
                printf("Echo %s to %s\n", buf,
                                          inet_ntoa(addr_client.sin_addr));
            } else if(readlen == 0) {
                printf("Disconnected %s\n", inet_ntoa(addr_client.sin_addr));
                close(sock_client);
                break;
            }
        }
    }

    return 0;
}
