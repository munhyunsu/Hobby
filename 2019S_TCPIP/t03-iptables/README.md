# iptables firewall

## iptables command example
- list all rules
```bash
iptables -L
```

- flush chain
```bash
iptables -F
```

- set the policy
```bash
iptables -P INPUT ACCEPT
```

- append rule
```bash
iptables -A INPUT -p tcp -dport 80 -j ACCEPT
```

