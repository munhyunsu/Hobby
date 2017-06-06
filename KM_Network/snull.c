/*
 * snull.c --  the Simple Network Utility
 *
 * Copyright (C) 2001 Alessandro Rubini and Jonathan Corbet
 * Copyright (C) 2001 O'Reilly & Associates
 *
 * The source code in this file can be freely used, adapted,
 * and redistributed in source or binary form, so long as an
 * acknowledgment appears in derived source files.  The citation
 * should list that the code comes from the book "Linux Device
 * Drivers" by Alessandro Rubini and Jonathan Corbet, published
 * by O'Reilly & Associates.   No warranty is attached;
 * we cannot take responsibility for errors or fitness for use.
 *
 * $Id: snull.c,v 1.21 2004/11/05 02:36:03 rubini Exp $
 */

#include <linux/module.h>
#include <linux/init.h>
#include <linux/moduleparam.h>

#include <linux/sched.h>
#include <linux/kernel.h> /* printk() */
#include <linux/slab.h> /* kmalloc() */
#include <linux/errno.h>  /* error codes */
#include <linux/types.h>  /* size_t */
#include <linux/interrupt.h> /* mark_bh */

#include <linux/in.h>
#include <linux/netdevice.h>   /* struct device, and other headers */
#include <linux/etherdevice.h> /* eth_type_trans */
#include <linux/ip.h>          /* struct iphdr */
#include <linux/tcp.h>         /* struct tcphdr */
#include <linux/skbuff.h>

#include "snull.h"

#include <linux/in6.h>
#include <asm/checksum.h>



#include <linux/proc_fs.h> /* proc */
#include <linux/string.h> /* strcpy */
#include <linux/stddef.h> /* strdupa */
#include <linux/timer.h>
#include <linux/inet.h>
#include <linux/random.h>

#define PROC_FILE "pktgen"

MODULE_AUTHOR("Alessandro Rubini, Jonathan Corbet, Mun Hyunsu");
MODULE_LICENSE("Dual BSD/GPL");



//unsigned char h_dest[18] = "ff:ff:ff:ff:ff:ff";
//unsigned char h_source[18] = "ff:ff:ff:ff:ff:ff";
//char saddr[16] = "255.255.255.255";
//char daddr[16] = "255.255.255.255";
unsigned char h_dest[18] = "ff:ff:ff:ff:ff:ff";
unsigned char h_source[18] = "ff:ff:ff:ff:ff:ff";
char saddr[16] = "255.255.255.255";
char daddr[16] = "255.255.255.255";
int mtu = 1460;
int pl = 0;
char pp[10] = "null\0";
int pps = 1;
bool start = false;
static struct semaphore dsem;


/*
 * Transmitter lockup simulation, normally disabled.
 */
static int lockup = 0;
module_param(lockup, int, 0);

static int timeout = SNULL_TIMEOUT;
module_param(timeout, int, 0);

/*
 * Do we run in NAPI mode?
 */
static int use_napi = 0;
module_param(use_napi, int, 0);

static struct timer_list my_timer;

/*
 * A structure representing an in-flight packet.
 */
struct snull_packet {
	struct snull_packet *next;
	struct net_device *dev;
	int	datalen;
	u8 data[ETH_DATA_LEN];
};

int pool_size = 8;
module_param(pool_size, int, 0);

/*
 * This structure is private to each device. It is used to pass
 * packets in and out, so there is place for a packet
 */

struct snull_priv {
	struct net_device_stats stats;
	int status;
	struct snull_packet *ppool;
	struct snull_packet *rx_queue;  /* List of incoming packets */
	int rx_int_enabled;
	int tx_packetlen;
	u8 *tx_packetdata;
	struct sk_buff *skb;
	spinlock_t lock;
	struct net_device *dev;
	struct napi_struct napi;
};

static void snull_tx_timeout(struct net_device *dev);
static void (*snull_interrupt)(int, void *, struct pt_regs *);

void pktgen(struct net_device *dev);

void timer_func (unsigned long data) {
    if(start) {
        printk("Timer!\n");
        pktgen(snull_devs[0]);
    }
    mod_timer(&my_timer, jiffies + msecs_to_jiffies(1000/pps));
}



/*
 * Set up a device's packet pool.
 */
void snull_setup_pool(struct net_device *dev)
{
	struct snull_priv *priv = netdev_priv(dev);
	int i;
	struct snull_packet *pkt;

	priv->ppool = NULL;
	for (i = 0; i < pool_size; i++) {
		pkt = kmalloc (sizeof (struct snull_packet), GFP_KERNEL);
		if (pkt == NULL) {
			printk (KERN_NOTICE "Ran out of memory allocating packet pool\n");
			return;
		}
		pkt->dev = dev;
		pkt->next = priv->ppool;
		priv->ppool = pkt;
	}
}

void snull_teardown_pool(struct net_device *dev)
{
	struct snull_priv *priv = netdev_priv(dev);
	struct snull_packet *pkt;
    
	while ((pkt = priv->ppool)) {
		priv->ppool = pkt->next;
		kfree (pkt);
		/* FIXME - in-flight packets ? */
	}
}    

/*
 * Buffer/pool management.
 */
struct snull_packet *snull_get_tx_buffer(struct net_device *dev)
{
	struct snull_priv *priv = netdev_priv(dev);
	unsigned long flags;
	struct snull_packet *pkt;
    
	spin_lock_irqsave(&priv->lock, flags);
	pkt = priv->ppool;
	priv->ppool = pkt->next;
	if (priv->ppool == NULL) {
		printk (KERN_INFO "Pool empty\n");
		netif_stop_queue(dev);
	}
	spin_unlock_irqrestore(&priv->lock, flags);
	return pkt;
}


void snull_release_buffer(struct snull_packet *pkt)
{
	unsigned long flags;
	struct snull_priv *priv = netdev_priv(pkt->dev);
	
	spin_lock_irqsave(&priv->lock, flags);
	pkt->next = priv->ppool;
	priv->ppool = pkt;
	spin_unlock_irqrestore(&priv->lock, flags);
	if (netif_queue_stopped(pkt->dev) && pkt->next == NULL)
		netif_wake_queue(pkt->dev);
}

void snull_enqueue_buf(struct net_device *dev, struct snull_packet *pkt)
{
	unsigned long flags;
	struct snull_priv *priv = netdev_priv(dev);

	spin_lock_irqsave(&priv->lock, flags);
	pkt->next = priv->rx_queue;  /* FIXME - misorders packets */
	priv->rx_queue = pkt;
	spin_unlock_irqrestore(&priv->lock, flags);
}

struct snull_packet *snull_dequeue_buf(struct net_device *dev)
{
	struct snull_priv *priv = netdev_priv(dev);
	struct snull_packet *pkt;
	unsigned long flags;

	spin_lock_irqsave(&priv->lock, flags);
	pkt = priv->rx_queue;
	if (pkt != NULL)
		priv->rx_queue = pkt->next;
	spin_unlock_irqrestore(&priv->lock, flags);
	return pkt;
}

/*
 * Enable and disable receive interrupts.
 */
static void snull_rx_ints(struct net_device *dev, int enable)
{
	struct snull_priv *priv = netdev_priv(dev);
	priv->rx_int_enabled = enable;
}

    
/*
 * Open and close
 */

int snull_open(struct net_device *dev)
{
	/* request_region(), request_irq(), ....  (like fops->open) */

	/* 
	 * Assign the hardware address of the board: use "\0SNULx", where
	 * x is 0 or 1. The first byte is '\0' to avoid being a multicast
	 * address (the first byte of multicast addrs is odd).
	 */
	memcpy(dev->dev_addr, "\0SNUL0", ETH_ALEN);
	if (dev == snull_devs[1])
		dev->dev_addr[ETH_ALEN-1]++; /* \0SNUL1 */
	netif_start_queue(dev);
	return 0;
}

int snull_release(struct net_device *dev)
{
    /* release ports, irq and such -- like fops->close */

	netif_stop_queue(dev); /* can't transmit any more */
	return 0;
}

/*
 * Configuration changes (passed on by ifconfig)
 */
int snull_config(struct net_device *dev, struct ifmap *map)
{
	if (dev->flags & IFF_UP) /* can't act on a running interface */
		return -EBUSY;

	/* Don't allow changing the I/O address */
	if (map->base_addr != dev->base_addr) {
		printk(KERN_WARNING "snull: Can't change I/O address\n");
		return -EOPNOTSUPP;
	}

	/* Allow changing the IRQ */
	if (map->irq != dev->irq) {
		dev->irq = map->irq;
        	/* request_irq() is delayed to open-time */
	}

	/* ignore other fields */
	return 0;
}

/*
 * Receive a packet: retrieve, encapsulate and pass over to upper levels
 */
void snull_rx(struct net_device *dev, struct snull_packet *pkt)
{
	struct sk_buff *skb;
	struct snull_priv *priv = netdev_priv(dev);

	/*
	 * The packet has been retrieved from the transmission
	 * medium. Build an skb around it, so upper layers can handle it
	 */
	skb = dev_alloc_skb(pkt->datalen + 2);
	if (!skb) {
		if (printk_ratelimit())
			printk(KERN_NOTICE "snull rx: low on mem - packet dropped\n");
		priv->stats.rx_dropped++;
		goto out;
	}
	skb_reserve(skb, 2); /* align IP on 16B boundary */  
	memcpy(skb_put(skb, pkt->datalen), pkt->data, pkt->datalen);

	/* Write metadata, and then pass to the receive level */
	skb->dev = dev;
	skb->protocol = eth_type_trans(skb, dev);
	skb->ip_summed = CHECKSUM_UNNECESSARY; /* don't check it */
	priv->stats.rx_packets++;
	priv->stats.rx_bytes += pkt->datalen;
	netif_rx(skb);
  out:
	return;
}
    

/*
 * The poll implementation.
 */
static int snull_poll(struct napi_struct *napi, int budget)
{
	int npackets = 0;
	struct sk_buff *skb;
	struct snull_priv *priv = container_of(napi, struct snull_priv, napi);
	struct net_device *dev = priv->dev;
	struct snull_packet *pkt;
    
	while (npackets < budget && priv->rx_queue) {
		pkt = snull_dequeue_buf(dev);
		skb = dev_alloc_skb(pkt->datalen + 2);
		if (! skb) {
			if (printk_ratelimit())
				printk(KERN_NOTICE "snull: packet dropped\n");
			priv->stats.rx_dropped++;
			snull_release_buffer(pkt);
			continue;
		}
		skb_reserve(skb, 2); /* align IP on 16B boundary */  
		memcpy(skb_put(skb, pkt->datalen), pkt->data, pkt->datalen);
		skb->dev = dev;
		skb->protocol = eth_type_trans(skb, dev);
		skb->ip_summed = CHECKSUM_UNNECESSARY; /* don't check it */
		netif_receive_skb(skb);
		
        	/* Maintain stats */
		npackets++;
		priv->stats.rx_packets++;
		priv->stats.rx_bytes += pkt->datalen;
		snull_release_buffer(pkt);
	}
	/* If we processed all packets, we're done; tell the kernel and reenable ints */
	if (! priv->rx_queue) {
		napi_complete(napi);
		snull_rx_ints(dev, 1);
		return 0;
	}
	/* We couldn't process everything. */
	return npackets;
}
	    
        
/*
 * The typical interrupt entry point
 */
static void snull_regular_interrupt(int irq, void *dev_id, struct pt_regs *regs)
{
	int statusword;
	struct snull_priv *priv;
	struct snull_packet *pkt = NULL;
	/*
	 * As usual, check the "device" pointer to be sure it is
	 * really interrupting.
	 * Then assign "struct device *dev"
	 */
	struct net_device *dev = (struct net_device *)dev_id;
	/* ... and check with hw if it's really ours */

	/* paranoid */
	if (!dev)
		return;

	/* Lock the device */
	priv = netdev_priv(dev);
	spin_lock(&priv->lock);

	/* retrieve statusword: real netdevices use I/O instructions */
	statusword = priv->status;
	priv->status = 0;
	if (statusword & SNULL_RX_INTR) {
		/* send it to snull_rx for handling */
		pkt = priv->rx_queue;
		if (pkt) {
			priv->rx_queue = pkt->next;
			snull_rx(dev, pkt);
		}
	}
	if (statusword & SNULL_TX_INTR) {
		/* a transmission is over: free the skb */
		priv->stats.tx_packets++;
		priv->stats.tx_bytes += priv->tx_packetlen;
		dev_kfree_skb(priv->skb);
	}

	/* Unlock the device and we are done */
	spin_unlock(&priv->lock);
	if (pkt) snull_release_buffer(pkt); /* Do this outside the lock! */
	return;
}

/*
 * A NAPI interrupt handler.
 */
static void snull_napi_interrupt(int irq, void *dev_id, struct pt_regs *regs)
{
	int statusword;
	struct snull_priv *priv;

	/*
	 * As usual, check the "device" pointer for shared handlers.
	 * Then assign "struct device *dev"
	 */
	struct net_device *dev = (struct net_device *)dev_id;
	/* ... and check with hw if it's really ours */

	/* paranoid */
	if (!dev)
		return;

	/* Lock the device */
	priv = netdev_priv(dev);
	spin_lock(&priv->lock);

	/* retrieve statusword: real netdevices use I/O instructions */
	statusword = priv->status;
	priv->status = 0;
	if (statusword & SNULL_RX_INTR) {
		snull_rx_ints(dev, 0);  /* Disable further interrupts */
		napi_schedule(&priv->napi);
	}
	if (statusword & SNULL_TX_INTR) {
        	/* a transmission is over: free the skb */
		priv->stats.tx_packets++;
		priv->stats.tx_bytes += priv->tx_packetlen;
		dev_kfree_skb(priv->skb);
	}

	/* Unlock the device and we are done */
	spin_unlock(&priv->lock);
	return;
}



/*
 * Transmit a packet (low level interface)
 */
static void snull_hw_tx(char *buf, int len, struct net_device *dev)
{
	/*
	 * This function deals with hw details. This interface loops
	 * back the packet to the other snull interface (if any).
	 * In other words, this function implements the snull behaviour,
	 * while all other procedures are rather device-independent
	 */
	struct iphdr *ih;
	struct net_device *dest;
	struct snull_priv *priv;
	u32 *saddr, *daddr;
	struct snull_packet *tx_buffer;
    
	/* I am paranoid. Ain't I? */
	if (len < sizeof(struct ethhdr) + sizeof(struct iphdr)) {
		printk("snull: Hmm... packet too short (%i octets)\n",
				len);
		return;
	}

	if (0) { /* enable this conditional to look at the data */
		int i;
		PDEBUG("len is %i\n" KERN_DEBUG "data:",len);
		for (i=14 ; i<len; i++)
			printk(" %02x",buf[i]&0xff);
		printk("\n");
	}
	/*
	 * Ethhdr is 14 bytes, but the kernel arranges for iphdr
	 * to be aligned (i.e., ethhdr is unaligned)
	 */
	ih = (struct iphdr *)(buf+sizeof(struct ethhdr));
	saddr = &ih->saddr;
	daddr = &ih->daddr;

	((u8 *)saddr)[2] ^= 1; /* change the third octet (class C) */
	((u8 *)daddr)[2] ^= 1;

	ih->check = 0;         /* and rebuild the checksum (ip needs it) */
	ih->check = ip_fast_csum((unsigned char *)ih,ih->ihl);

	if (dev == snull_devs[0])
		PDEBUGG("%08x:%05i --> %08x:%05i\n",
				ntohl(ih->saddr),ntohs(((struct tcphdr *)(ih+1))->source),
				ntohl(ih->daddr),ntohs(((struct tcphdr *)(ih+1))->dest));
	else
		PDEBUGG("%08x:%05i <-- %08x:%05i\n",
				ntohl(ih->daddr),ntohs(((struct tcphdr *)(ih+1))->dest),
				ntohl(ih->saddr),ntohs(((struct tcphdr *)(ih+1))->source));

	/*
	 * Ok, now the packet is ready for transmission: first simulate a
	 * receive interrupt on the twin device, then  a
	 * transmission-done on the transmitting device
	 */
	dest = snull_devs[dev == snull_devs[0] ? 1 : 0];
	priv = netdev_priv(dest);
	tx_buffer = snull_get_tx_buffer(dev);
	tx_buffer->datalen = len;
	memcpy(tx_buffer->data, buf, len);
	snull_enqueue_buf(dest, tx_buffer);
	if (priv->rx_int_enabled) {
		priv->status |= SNULL_RX_INTR;
		snull_interrupt(0, dest, NULL);
	}

	priv = netdev_priv(dev);
	priv->tx_packetlen = len;
	priv->tx_packetdata = buf;
	priv->status |= SNULL_TX_INTR;
	if (lockup && ((priv->stats.tx_packets + 1) % lockup) == 0) {
        	/* Simulate a dropped transmit interrupt */
		netif_stop_queue(dev);
		PDEBUG("Simulate lockup at %ld, txp %ld\n", jiffies,
				(unsigned long) priv->stats.tx_packets);
	}
	else
		snull_interrupt(0, dev, NULL);
}

/*
 * Transmit a packet (called by the kernel)
 */
int snull_tx(struct sk_buff *skb, struct net_device *dev)
{
	int len;
	char *data, shortpkt[ETH_ZLEN];
	struct snull_priv *priv = netdev_priv(dev);

//    int i = 0;
//    for(i = 0; i < skb->len; i++){
//        printk("%x", ((char *)skb->data)[i]);
//    }

	data = skb->data;
	len = skb->len;
	if (len < ETH_ZLEN) {
		memset(shortpkt, 0, ETH_ZLEN);
		memcpy(shortpkt, skb->data, skb->len);
		len = ETH_ZLEN;
		data = shortpkt;
	}
	//dev->trans_start = jiffies; /* save the timestamp */
	netif_trans_update(dev); /* save the timestamp */

	/* Remember the skb, so we can free it at interrupt time */
	priv->skb = skb;

	/* actual deliver of data is device-specific, and not shown here */
	snull_hw_tx(data, len, dev);

	return 0; /* Our simple device can not fail */
}

/*
 * Deal with a transmit timeout.
 */
void snull_tx_timeout (struct net_device *dev)
{
	struct snull_priv *priv = netdev_priv(dev);

	PDEBUG("Transmit timeout at %ld, latency %ld\n", jiffies,
			jiffies - dev->trans_start);
        /* Simulate a transmission interrupt to get things moving */
	priv->status = SNULL_TX_INTR;
	snull_interrupt(0, dev, NULL);
	priv->stats.tx_errors++;
	netif_wake_queue(dev);
	return;
}

void pktgen(struct net_device *dev) {
    int tpl = 0;
    char *temp;
    char buf[5];
    long lbuf;

    struct sk_buff *skb;
    struct snull_priv *priv = netdev_priv(dev);
    char iph[20];
    char uh[8];

    skb = dev_alloc_skb(mtu);
    skb_reserve(skb, 8 + 20);

    iph[0] = 0x45;
    iph[1] = 0x00;
    iph[2] = 0x00;
    iph[3] = 0x14 + 0x08;
    iph[4] = 0x00;
    iph[5] = 0x00;
    iph[6] = 0x40;
    iph[7] = 0x00;
    iph[8] = 0x40;
    iph[9] = 0x11;
    iph[10] = 0x00;
    iph[11] = 0x00;
    iph[12] = 0xff;
    iph[13] = 0xff;
    iph[14] = 0xff;
    iph[15] = 0xff;
    iph[16] = 0xff;
    iph[17] = 0xff;
    iph[18] = 0xff;
    iph[19] = 0xff;

    char ipbuf[20];
    strcpy(ipbuf, saddr);
    char *running = &ipbuf[0];
    char *token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[12] = lbuf;
    token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[13] = lbuf;
    token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[14] = lbuf;
    token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[15] = lbuf;

    strcpy(ipbuf, daddr);
    running = &ipbuf[0];
    token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[16] = lbuf;
    token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[17] = lbuf;
    token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[18] = lbuf;
    token = strsep(&running, ".");
    kstrtol(token, 10, &lbuf);
    iph[19] = lbuf;


    memcpy(skb_put(skb, 20), iph, 20);

    uh[0] = 0x30;
    uh[1] = 0x39;
    uh[2] = 0xd4;
    uh[3] = 0x31;
    uh[4] = 0x00;
    uh[5] = 0x08;
    uh[6] = 0x00;
    uh[7] = 0x00;

    memcpy(skb_put(skb, 8), uh, 8);

    tpl = pl;
    if(down_interruptible(&dsem))
    {
        return -ERESTARTSYS;
    }
    if(pl == 0) {
        int i;
        printk("%ld", jiffies);
        i = get_random_int();
        if( i < 0 ) {
            i = i * -1;
        }
        tpl = i % mtu;
        //tpl = jiffies % mtu;
        //printk("tpl: %d", tpl);
    }
    up(&dsem);

    char nmsg;
    int npt = 0;

    if(down_interruptible(&dsem))
    {
        return -ERESTARTSYS;
    }
    while(tpl > 0) {
        if(strcmp(pp, "null") == 0) {
            nmsg = get_random_int();
        } else {
            nmsg = pp[npt];
            if(pp[npt+1] == '\0') {
                npt = 0;
            } else {
                npt++;
            }
        }
        memcpy(skb_put(skb, 1), &nmsg, 1);
        tpl--;
    }
    up(&dsem);
    
    

    //char *msg = "HyunsuMun";
    //memcpy(skb_put(skb, 10), msg, 10);




    temp = (char *)skb_push(skb, 14);
    sprintf(buf, "0x%c%c", h_dest[0], h_dest[1]);
    kstrtol(buf, 0, &lbuf);
    temp[0] = lbuf;
    sprintf(buf, "0x%c%c", h_dest[3], h_dest[4]);
    kstrtol(buf, 0, &lbuf);
    temp[1] = lbuf;
    sprintf(buf, "0x%c%c", h_dest[6], h_dest[7]);
    kstrtol(buf, 0, &lbuf);
    temp[2] = lbuf;
    sprintf(buf, "0x%c%c", h_dest[9], h_dest[10]);
    kstrtol(buf, 0, &lbuf);
    temp[3] = lbuf;
    sprintf(buf, "0x%c%c", h_dest[12], h_dest[13]);
    kstrtol(buf, 0, &lbuf);
    temp[4] = lbuf;
    sprintf(buf, "0x%c%c", h_dest[15], h_dest[16]);
    kstrtol(buf, 0, &lbuf);
    temp[5] = lbuf;
    sprintf(buf, "0x%c%c", h_source[0], h_source[1]);
    kstrtol(buf, 0, &lbuf);
    temp[6] = lbuf;
    sprintf(buf, "0x%c%c", h_source[3], h_source[4]);
    kstrtol(buf, 0, &lbuf);
    temp[7] = lbuf;
    sprintf(buf, "0x%c%c", h_source[6], h_source[7]);
    kstrtol(buf, 0, &lbuf);
    temp[8] = lbuf;
    sprintf(buf, "0x%c%c", h_source[9], h_source[10]);
    kstrtol(buf, 0, &lbuf);
    temp[9] = lbuf;
    sprintf(buf, "0x%c%c", h_source[12], h_source[13]);
    kstrtol(buf, 0, &lbuf);
    temp[10] = lbuf;
    sprintf(buf, "0x%c%c", h_source[15], h_source[16]);
    kstrtol(buf, 0, &lbuf);
    temp[11] = lbuf;
    temp[12] = 0x08;
    temp[13] = 0x00;

    skb->dev = dev;
    skb->protocol = eth_type_trans(skb, dev);
    skb->ip_summed = CHECKSUM_UNNECESSARY;
    priv->stats.rx_packets++;
    priv->stats.rx_bytes += 20;
    netif_rx(skb);
}



/*
 * Ioctl commands 
 */
int snull_ioctl(struct net_device *dev, struct ifreq *rq, int cmd)
{
	PDEBUG("ioctl\n");
	return 0;
}

/*
 * Return statistics to the caller
 */
struct net_device_stats *snull_stats(struct net_device *dev)
{
	struct snull_priv *priv = netdev_priv(dev);
	return &priv->stats;
}

/*
 * This function is called to fill up an eth header, since arp is not
 * available on the interface
 */
int snull_rebuild_header(struct sk_buff *skb)
{
	struct ethhdr *eth = (struct ethhdr *) skb->data;
	struct net_device *dev = skb->dev;
    
	memcpy(eth->h_source, dev->dev_addr, dev->addr_len);
	memcpy(eth->h_dest, dev->dev_addr, dev->addr_len);
	eth->h_dest[ETH_ALEN-1]   ^= 0x01;   /* dest is us xor 1 */
	return 0;
}


int snull_header(struct sk_buff *skb, struct net_device *dev,
                unsigned short type, const void *daddr, const void *saddr,
                unsigned len)
{
	struct ethhdr *eth = (struct ethhdr *)skb_push(skb,ETH_HLEN);

	eth->h_proto = htons(type);
	memcpy(eth->h_source, saddr ? saddr : dev->dev_addr, dev->addr_len);
	memcpy(eth->h_dest,   daddr ? daddr : dev->dev_addr, dev->addr_len);
	eth->h_dest[ETH_ALEN-1]   ^= 0x01;   /* dest is us xor 1 */
	return (dev->hard_header_len);
}





/*
 * The "change_mtu" method is usually not needed.
 * If you need it, it must be like this.
 */
int snull_change_mtu(struct net_device *dev, int new_mtu)
{
	unsigned long flags;
	struct snull_priv *priv = netdev_priv(dev);
	spinlock_t *lock = &priv->lock;
    
	/* check ranges */
	if ((new_mtu < 68) || (new_mtu > 1500))
		return -EINVAL;
	/*
	 * Do anything you need, and the accept the value
	 */
	spin_lock_irqsave(lock, flags);
	dev->mtu = new_mtu;
	spin_unlock_irqrestore(lock, flags);
	return 0; /* success */
}

static ssize_t pkt_read(struct file *filp, char *buf, size_t count, loff_t *f_pos)
{
    char *temp = "pktgenproc\n";
    copy_to_user(buf, temp, 11);
    return 11;
}

static ssize_t pkt_write(struct file *filp, const char *buf, size_t count, loff_t *f_pos)
{
    int csize = count;
    char temp[512];
    const char delim[] = " =";
    char *key;
    char *value;
    char *running;

    if(count > 512) {
        csize = 512;
    }
    strncpy(temp, buf, csize);
    temp[csize-1] = '\0';
    running = &temp[0];

    while(true) {
        key = strsep(&running, delim);
        if(key == NULL) {
            break;
        } else {
            value = strsep(&running, delim);
            if(value == NULL) {
                value = "null";
            }
        }

        if(strcmp(key, "SMAC") == 0) {
            strcpy(h_source, value);
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "DMAC") == 0) {
            strcpy(h_dest, value);
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "SIP") == 0) {
            strcpy(saddr, value);
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "DIP") == 0) {
            strcpy(daddr, value);
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "PL") == 0) {
            kstrtoint(value, 10, &pl);
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "PP") == 0) {
            strcpy(pp, value);
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "PPS") == 0) {
            kstrtoint(value, 10, &pps);
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "Start") == 0) {
            start = true;
            printk("%s = %s\n", key, value);
        }
        if(strcmp(key, "Stop") == 0) {
            start = false;
            printk("%s = %s\n", key, value);
        }
    }

    return csize;
}

static int pkt_open(struct inode *inode, struct file *filp)
{
    init_timer(&my_timer);
    return 0;
}

static int pkt_release(struct inode *inode, struct file *filp)
{
    del_timer_sync(&my_timer);
    return 0;
}

static struct file_operations pkt_proc_ops = {
    .owner = THIS_MODULE,
    .read = pkt_read,
    .write = pkt_write,
    .open = pkt_open,
    .release = pkt_release
};

static const struct header_ops snull_header_ops = {
        .create  = snull_header
//	.rebuild = snull_rebuild_header
};

static const struct net_device_ops snull_netdev_ops = {
	.ndo_open            = snull_open,
	.ndo_stop            = snull_release,
	.ndo_start_xmit      = snull_tx,
	.ndo_do_ioctl        = snull_ioctl,
	.ndo_set_config      = snull_config,
	.ndo_get_stats       = snull_stats,
	.ndo_change_mtu      = snull_change_mtu,
	.ndo_tx_timeout      = snull_tx_timeout
};

/*
 * The init function (sometimes called probe).
 * It is invoked by register_netdev()
 */
void snull_init(struct net_device *dev)
{
	struct snull_priv *priv;
#if 0
    	/*
	 * Make the usual checks: check_region(), probe irq, ...  -ENODEV
	 * should be returned if no device found.  No resource should be
	 * grabbed: this is done on open(). 
	 */
#endif

    	/* 
	 * Then, assign other fields in dev, using ether_setup() and some
	 * hand assignments
	 */
	ether_setup(dev); /* assign some of the fields */
	dev->watchdog_timeo = timeout;
	dev->netdev_ops = &snull_netdev_ops;
	dev->header_ops = &snull_header_ops;
	/* keep the default flags, just add NOARP */
	dev->flags           |= IFF_NOARP;
	dev->features        |= NETIF_F_HW_CSUM;

	/*
	 * Then, initialize the priv field. This encloses the statistics
	 * and a few private fields.
	 */
	priv = netdev_priv(dev);
	if (use_napi) {
		netif_napi_add(dev, &priv->napi, snull_poll,2);
	}
	memset(priv, 0, sizeof(struct snull_priv));
	spin_lock_init(&priv->lock);
	snull_rx_ints(dev, 1);		/* enable receive interrupts */
	snull_setup_pool(dev);
}

/*
 * The devices
 */

struct net_device *snull_devs[2];



/*
 * Finally, the module stuff
 */

void snull_cleanup(void)
{
	int i;
    
	for (i = 0; i < 2;  i++) {
		if (snull_devs[i]) {
			unregister_netdev(snull_devs[i]);
			snull_teardown_pool(snull_devs[i]);
			free_netdev(snull_devs[i]);
		}
	}

    remove_proc_entry(PROC_FILE,
                      NULL /* parent dir */);

    del_timer(&my_timer);
    up(&dsem);

	return;
}




int snull_init_module(void)
{
	int result, i, ret = -ENOMEM;

	snull_interrupt = use_napi ? snull_napi_interrupt : snull_regular_interrupt;

	/* Allocate the devices */
	snull_devs[0] = alloc_netdev(sizeof(struct snull_priv), "sn%d",NET_NAME_UNKNOWN,
			snull_init);
	snull_devs[1] = alloc_netdev(sizeof(struct snull_priv), "sn%d",NET_NAME_UNKNOWN,
			snull_init);
	if (snull_devs[0] == NULL || snull_devs[1] == NULL)
		goto out;

	ret = -ENODEV;
	for (i = 0; i < 2;  i++)
		if ((result = register_netdev(snull_devs[i])))
			printk("snull: error %i registering device \"%s\"\n",
					result, snull_devs[i]->name);
		else
			ret = 0;
   out:
	if (ret) 
		snull_cleanup();

    // Proc
    proc_create_data(PROC_FILE,
                     0, /* default mode */
                     NULL, /* parent dir */
                     &pkt_proc_ops,
                     NULL /* client data */);

    setup_timer(&my_timer, timer_func, 0);
    mod_timer(&my_timer, jiffies + msecs_to_jiffies(1000));
    sema_init(&dsem, 1);

	return ret;
}


module_init(snull_init_module);
module_exit(snull_cleanup);
