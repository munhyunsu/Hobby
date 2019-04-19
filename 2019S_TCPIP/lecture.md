# Advanced TCP/IP

## What is autonomous system(AS)

### IP address range
```bash
whois 168.188.0.0
```

### AS number
```bash
whois -a 168.188.1.1
```

### Server location (Link layer)
```bash
dig www.google.com
nslookup www.google.com
traceroute -n 172.217.161.36
```

### Domain to address
```bash
dig @8.8.8.8 www.google.com
```
- With trace
```bash
dig @8.8.8.8 computer.cnu.ac.kr +trace
```

### Route table
```bash
netstat -rn
```

## Addressing

### Need to remember
- CIDR
  - Start / End address
- Netmask
- Subnet

### Zone transfer
```bash
dig axfr @168.188.1.1 cnu.ac.kr
```
```bash
host ftp.rfc-editor.org
host -t any www.whitehouse.gov
host -t ptr 208.xxx
```

## CSMA/CD
- Carrior Sence Multiple Access / Collision Detection

## Distributed Distributed Coordination Function: CSMA/CA
- Carrior Sence Multiple Access / Collision Avoidance
- RTS: Request to Send
- CTS: Clear to Send
- ACK: Acknowledgement

### Hidden Terminal Problem
- A -- B -- C
- Solved by RTS/CTS

## IP

### Important things
- Src/Dst IP Address
- Protocol / Next header
- Time-to-Live / Hop Limit

### Maximum Transmission Unit
- Ethernet: 1500 Bytes
- IP: 65535 Bytes
- Flagmentation: Identification, Don't flagment, Flagmentation

## ICMP
- Not data transfer protocol, it is alert or notify information protocol

### IP control protocol
- ping, traceroute

### ICMP Type
- [ping] Echo Request(128) / Echo Reply(129)
- [traceroute] Time exceeded(3) / Destination unreachable(1)
  - used TTL(IPv4) or Hop limit(IPv6) field

### traceroute
- Send a UDP packet with TTL field 1, 2, 3, ...
- If the router receive expired packet then reply time exceeded ICMP packet to sender
- The last hop(target server) send a destination unreachable packet

### The packet size over MTU
- ICMP packet

## UDP

## TCP
- Ethernet CSMA/CD: manage medium
- Retransmission in TCP: manage error

### ARQ and Retransmission

### Delay
1. Processing
2. Propagation
3. Transmit
4. Queueing: Not constant
  - Packet switching network
  - Non circuit switching network

### Flow control vs Congestion control
- Flow control
  - Rate-based vs. window-based
  - Receiver's signal: window update
- Congestion control
  - Implicit signal

### RTT timer
- The average changes
  - Statistical process
  - True RTT

### TCP sequence number
- 2^32: 4,294,967,296
  - 4G bytes file size

### TCP Payload
- 1.4K bytes
  - 1460 bytes

### TCP checksum
- Calculate with header and payload

### TCP options
- Window scale: the default size which are 64K bytes is too small
  - It is in only SYN packet
- Maximum segment size: It is not a negotiation
  - It is a limit
  - MSS option is in only SYN packet
- SACK
  - A pair of 32-bit sequence
  - n SACK block (n8+2)

### RTO: Retransmission timer
- use variance
  - Classic version
  - Standard version
- Retransmission ambiguity
  - Karn's algorithm
  - Ignore retransmitted segments
  - Timestamp option
- Nagle algorithm
  - bulk data transfer
  - application such as ssh was not applied

### TCP persist timer
- Ask client's window size

### Silly window syndrome (SW)
- Avoidance
  - Receiver: small windows are not advertised
  - Sender: small segment are not sent

## IGMP: Internet group management protocol
- IP multicast: IGMP

## PPP
- DSL: Digital subscriber line
  - Digital multiplexer
  - Using telephone line, it create data link line
- At nowadays, PPP was used at VPN called PPTP
  - Point-to-Point Tunneling Protocol

### GRE(Genegic Routing Encapsulation)

### Van jacobson
- tcpdump
- traceroute
- TCP/IP compression
- Need to read white paper
