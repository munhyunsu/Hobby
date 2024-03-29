# Command history

# Create Root CA Certificates

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

```
Country Name (2 letter code) [AU]:KR
State or Province Name (full name) [Some-State]:Daejeon
Locality Name (eg, city) []:Yuseong
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Chungnam National University
Organizational Unit Name (eg, section) []:Data Network Laboratory
Common Name (e.g. server FQDN or YOUR name) []:DNLab
Email Address []:munhyunsu@gmail.com
```

4. Verify certificate

```bash
openssl x509 -noout -text -in certs/cacert.pem
```

# Create Intermediate CA Certificates

1. Copy `openssl.cnf` to `ca_intermediate.cnf

```bash
cp /etc/ssl/openssl.cnf ./ca_intermediate.cnf
```

2. Create private key with strong encryption

```bash
mkdir IntermediateCA
cd IntermediateCA
mkdir certs crl newcerts private
chmod 700 private
touch index.txt
echo 1000 > serial
echo 1000 > crlnumber
openssl genrsa -aes256 -out ./LuHaCA/private/cakey.pem 4096
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

# References

- [OpenSSL](https://openssl-ca.readthedocs.io/)

