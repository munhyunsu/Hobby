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

