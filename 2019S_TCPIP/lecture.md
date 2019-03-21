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

### 



