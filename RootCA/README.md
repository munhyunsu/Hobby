# Command history

1. Copy `openssl.cnf` to `ca_root.cnf`

```bash
cp /etc/ssl/openssl.cnf ./ca_root.cnf
```

2. Create private key with strong encryption

```bash
mkdir RootCA
cd RootCA
mkdir certs crl newcerts private
chmod 700 private
touch index.txt
echo 1000 > serial
openssl genrsa -aes256 -out private/cakey.pem 8192
chmod 400 private/cakey.pem
```

3. Create Root CA Certificate

```bash
openssl req -config ca_root.cnf -key private/cakey.pem -new -x509 -days 7300 -sha256 -extensions v3_ca -out certs/cacert.pem
chmod 444 certs/cacert.pem
```

# References

- [OpenSSL](https://openssl-ca.readthedocs.io/)

