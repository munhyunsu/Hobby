# Command history

# Create Root CA Certificates

1. Copy `openssl.cnf` to `ca_root.cnf`

```bash
cp /etc/ssl/openssl.cnf ./ca_root.cnf
```

2. Create private key with strong encryption

```bash
openssl genrsa -aes256 -out private.keypw 4096
```

3. Create Root CA Certificate

```bash
openssl req -config openssl.cnf -key private.keypw -new -x509 -days 1825 -sha256 -extensions v3_ca -out ca_root.crt
```

4. Verify certificate

```bash
openssl x509 -noout -text -in ca_root.crt
```

# Create Intermediate CA Certificates

1. Copy `openssl.cnf` to `ca_intermediate.cnf

```bash
cp /etc/ssl/openssl.cnf ./ca_intermediate.cnf
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


