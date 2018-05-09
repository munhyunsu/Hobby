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
    int sock; // Socket descriptor
    struct sockaddr_in addr_server; // Server IP address
    unsigned short port_server; // Server port
    char echostr[BUFFSIZE]; // echo buffer
    unsigned int echolen; // echo buffer length
    char buf[BUFFSIZE]; // read buffer
    unsigned int buflen; // echo string length
    int readlen, totalreadlen; // readed buf length

    /* arguments parsing */
    if(argc != 3) { // check server port as arguments
        printf("Usage: a.out [SERVERIP] [SERVERPORT]\n");
        exit(1);
    }

    /* create socket */
    if( (sock = /* NEEDFIX: create socket (same as server)*/socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        printf("socket() error\n");
        exit(1);
    }

    /* server address structing */
    memset(&addr_server, 0, sizeof(addr_server)); // zero set
    addr_server.sin_family = AF_INET; // Internet address family
    addr_server.sin_addr.s_addr = inet_addr(argv[1]); // any interface
    addr_server.sin_port = htons(atoi(argv[2])); // port number

    /* connect socket to address and port */
    if( /* NEEDFIX: connect */connect(sock, (struct sockaddr *) &addr_server, 
            sizeof(addr_server)) < 0) {
        printf("connect() error\n");
        exit(1);
    }

    /* send string */
    while(1) {
        printf("Echo string: ");
        scanf("%s", echostr);
        if( strcmp(echostr, "exit") == 0 ) {
            break;
        }
        echolen = strlen(echostr);
        
        if( /*NEEDFIX: send string */send(sock, echostr, echolen, 0) != echolen ) {
            printf("send() error\n");
            exit(1);
        }

        totalreadlen = 0; // init
        printf("Echoed: ");
        while(totalreadlen < echolen) {
            if( (readlen = /* NEEDFIX: recv */recv(sock, buf, BUFFSIZE-1, 0)) <= 0) {
                printf("recv() error\n");
                exit(1);
            }
            totalreadlen = totalreadlen + readlen;
            buf[readlen] = '\0'; // null
            printf("%s", buf);
        }
        printf("\n");
    }

    close(sock);

    return 0;
}
