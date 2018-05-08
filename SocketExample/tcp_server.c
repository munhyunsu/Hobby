/*
  Socket example: server
*/
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
    /* prepare local variables */
    int sock_server, sock_client; // Socket descriptor
    struct sockaddr_in addr_server, addr_client; // Addresses
    unsigned short port_server; // Port number of server
    unsigned int client_addr_len; // client address structure

    /* arguments parsing */
    if(argc != 2) { // check server port as arguments
        printf("Usage: a.out [SERVERPORT]\n");
        exit(1);
    }
    port_server = atoi(argv[1]); // port number

    /* create socket */
    if( (sock_server = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0) {
        printf("socket() error\n");
        exit(1);
    }

    /* server address structing */
    memset(&addr_server, 0, sizeof(addr_server)) // zero set
    sddr_server.sin_family = AF_INET; // Internet address family
    addr_server.sin_addr.s_addr = htonl(INADDR_ANY); // any interface
    addr_server.sin_port = htons(port_server) // port number

    /* bind socket to address and port */
    if( bind(sock_server, (struct sockaddr *) &addr_server, 
            sizeof(addr_server)) < 0) {
        printf("bind() error\n");
        exit(1);
    }

    /* listen connection */
    



    return 0;
}
