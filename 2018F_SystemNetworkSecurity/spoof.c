/* For Problem 8 only
*  Sniff and spoof icmp packet   */

#define APP_NAME    "sniffex"
#define APP_DESC		"Sniffer example using libpcap"
#define APP_COPYRIGHT	"Copyright (c) 2006 The Tcpdump Group"
#define APP_DISCLAIMER	"THERE IS ABSOLUTELY NO WARRANTY FOR THIS PROGRAM."

#include <pcap.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <net/ethernet.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <arpa/inet.h>

/* default snap length (maximum bytes per packet to capture) */
#define SNAP_LEN 1518

/* ethernet headers are always exactly 14 bytes [1] */
#define SIZE_ETHERNET sizeof(struct ethhdr)

/* Spoofed packet containing only IP and ICMP headers */
struct spoof_packet
{
    struct ip iph;
    struct icmp icmph;
};


void
got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet);

void
print_app_banner(void);

void
print_app_usage(void);

/*
 * app name/banner
 */
void
print_app_banner(void)
{

	printf("%s - %s\n", APP_NAME, APP_DESC);
	printf("%s\n", APP_COPYRIGHT);
	printf("%s\n", APP_DISCLAIMER);
	printf("\n");

return;
}


/*
 * print help text
 */
void
print_app_usage(void)
{

	printf("Usage: %s [interface]\n", APP_NAME);
	printf("\n");
	printf("Options:\n");
	printf("    interface    Listen on <interface> for packets.\n");
	printf("\n");

return;
}

/* 
 * Generates ip/icmp header checksums using 16 bit words. nwords is number of 16 bit words
 */
unsigned short in_cksum(unsigned short *addr, int len)
{
	int nleft = len;
	int sum = 0;
	unsigned short *w = addr;
	unsigned short answer = 0;

	while (nleft > 1) {
		sum += *w++;
		nleft -= 2;
	}

	if (nleft == 1) {
		*(unsigned char *) (&answer) = *(unsigned char *) w;
		sum += answer;
	}
	
	sum = (sum >> 16) + (sum & 0xFFFF);
	sum += (sum >> 16);
	answer = ~sum;
	return (answer);
}

/*
 * dissect/print packet
 */
void
got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{

	static int count = 1;                   /* packet counter */

	int s;	// socket
	const int on = 1;

	/* declare pointers to packet headers */
	const struct ether_header *ethernet = (struct ether_header*)(packet);
	const struct ip *iph;              /* The IP header */
	const struct icmp *icmph;            /* The ICMP header */
	struct sockaddr_in dst;

	int size_ip;
	
	/* define/compute ip header offset */
	iph = (struct ip*)(packet + SIZE_ETHERNET);
	size_ip = iph->ip_hl*4;	// size of ip header

	if (iph->ip_p != IPPROTO_ICMP || size_ip < 20) {  // disregard other packets
		return;
	}
	
	/* define/compute icmp header offset */
	icmph = (struct icmp*)(packet + SIZE_ETHERNET + size_ip);
        
	/* print source and destination IP addresses */
	printf("%d) ICMP Sniff: from--%s\n", count, inet_ntoa(iph->ip_src) );  	
		
	/* Construct the spoof packet and allocate memory with the lengh of the datagram */
	char buf[htons(iph->ip_len)];
	struct spoof_packet *spoof = (struct spoof_packet *) buf;

	/* Initialize the structure spoof by copying everything in request packet to spoof packet*/
	memcpy(buf, iph, htons(iph->ip_len));
	/* Modify ip header */

   	//swap the destination ip address and source ip address
	(spoof->iph).ip_src = iph->ip_dst;
	(spoof->iph).ip_dst = iph->ip_src;

    	//recompute the checksum, you can leave it to 0 here since RAW socket will compute it for you.
	(spoof->iph).ip_sum = 0;

	/* Modify icmp header */
	
	// set the spoofed packet as echo-reply
	(spoof->icmph).icmp_type = ICMP_ECHOREPLY;
	// always set code to 0
	(spoof->icmph).icmp_code = 0;

	(spoof->icmph).icmp_cksum = 0;	// should be set as 0 first to recalculate.
	(spoof->icmph).icmp_cksum = in_cksum((unsigned short *) &(spoof->icmph), sizeof(spoof->icmph));
	//print the forged packet information
	printf("forged packet src is %s\n",inet_ntoa((spoof->iph).ip_src));
	printf("forged packet det is %s\n\n",inet_ntoa((spoof->iph).ip_dst));        
  	
	memset(&dst, 0, sizeof(dst));
    	dst.sin_family = AF_INET;
        dst.sin_addr.s_addr = (spoof->iph).ip_dst.s_addr;

	/* create RAW socket */
	if((s = socket(AF_INET, SOCK_RAW, IPPROTO_RAW)) < 0) {
        printf("socket() error");
		return;
	}
 
	/* socket options, tell the kernel we provide the IP structure */
	if(setsockopt(s, IPPROTO_IP, IP_HDRINCL, &on, sizeof(on)) < 0) {
		printf("setsockopt() for IP_HDRINCL error");
		return;
	}

	if(sendto(s, buf, sizeof(buf), 0, (struct sockaddr *) &dst, sizeof(dst)) < 0) {
		printf("sendto() error");
	}

	close(s);	// free resource
	
	//free(buf);
	count++; 
return;
}

int main(int argc, char **argv)
{

	char *dev = NULL;			/* capture device name */
	char errbuf[PCAP_ERRBUF_SIZE];		/* error buffer */
	pcap_t *handle;				/* packet capture handle */

	char filter_exp[] = "icmp[icmptype]=icmp-echo";		/* filter expression [3] */
	struct bpf_program fp;			/* compiled filter program (expression) */
	bpf_u_int32 mask;			/* subnet mask */
	bpf_u_int32 net;			/* ip */
	int num_packets = -1;			/* number of packets to capture, set -1 to capture all */

	print_app_banner();

	/* check for capture device name on command-line */
	if (argc == 2) {
		dev = argv[1];
	}
	else if (argc > 2) {
		fprintf(stderr, "error: unrecognized command-line options\n\n");
		print_app_usage();
		exit(EXIT_FAILURE);
	}
	else {
		/* find a capture device if not specified on command-line */
		dev = pcap_lookupdev(errbuf);
		if (dev == NULL) {
			fprintf(stderr, "Couldn't find default device: %s\n",
			    errbuf);
			exit(EXIT_FAILURE);
		}
	}
	
	/* get network number and mask associated with capture device */
	if (pcap_lookupnet(dev, &net, &mask, errbuf) == -1) {
		fprintf(stderr, "Couldn't get netmask for device %s: %s\n",
		    dev, errbuf);
		net = 0;
		mask = 0;
	}

	/* print capture info */
	printf("Device: %s\n", dev);
	printf("Number of packets: %d\n", num_packets);
	printf("Filter expression: %s\n", filter_exp);

	/* open capture device */
	handle = pcap_open_live(dev, SNAP_LEN, 1, 1000, errbuf);
	if (handle == NULL) {
		fprintf(stderr, "Couldn't open device %s: %s\n", dev, errbuf);
		exit(EXIT_FAILURE);
	}

	/* make sure we're capturing on an Ethernet device [2] */
	if (pcap_datalink(handle) != DLT_EN10MB) {
		fprintf(stderr, "%s is not an Ethernet\n", dev);
		exit(EXIT_FAILURE);
	}

	/* compile the filter expression */
	if (pcap_compile(handle, &fp, filter_exp, 0, net) == -1) {
		fprintf(stderr, "Couldn't parse filter %s: %s\n",
		    filter_exp, pcap_geterr(handle));
		exit(EXIT_FAILURE);
	}

	/* apply the compiled filter */
	if (pcap_setfilter(handle, &fp) == -1) {
		fprintf(stderr, "Couldn't install filter %s: %s\n",
		    filter_exp, pcap_geterr(handle));
		exit(EXIT_FAILURE);
	}

	/* now we can set our callback function */
	pcap_loop(handle, num_packets, got_packet, NULL);

	/* cleanup */
	pcap_freecode(&fp);
	pcap_close(handle);

	printf("\nCapture complete.\n");

return 0;
}
