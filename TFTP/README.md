# TFTP for installing OpenWRT

## Requirements
- Ubuntu server
- tftpd-hpa

## Steps
- [Ref](https://help.ubuntu.com/community/TFTP)
```bash
sudo cp /etc/default/tftpd-hpa /etc/default/tftpd-hpa.ORIGINAL
sudo vi /etc/default/tftpd-hpa
```

- Change conf
```bash
TFTP\_OPTIONS="--secure" to TFTP_OPTIONS="--secure --create"
```

- root dir
```bash
sudo chown -R tftp /var/lib/tftpboot
```
