# Command history

# Create Root CA Certificates

1. Copy `openssl.cnf` to `ca_root.cnf`

```bash
cp /etc/ssl/openssl.cnf .
```

2. Create private key with strong encryption

```bash
openssl genrsa -aes256 -out private.keypw 4096
```

# Create Self-signed certificates

1. Generate private key for RootCA

```bash
openssl genrsa -aes256 -out server.keypw 2048
```

2. Copy `openssl.cnf`

```bash
cp /etc/ssl/openssl.cnf ./
```

3. Create certificate-signing request

```bash
openssl req -new -config openssl.cnf -key server.keypw -out server.csr
```

4. Self signing cerficitate

```
openssl x509 -req -days 1825 -in server.csr -signkey server.keypw -out server.crt
```


