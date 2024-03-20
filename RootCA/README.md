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

# References

- [OpenSSL](https://openssl-ca.readthedocs.io/)

