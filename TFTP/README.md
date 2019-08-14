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

## Archer C7 v5 (KR) bug
  - Special id missing
  - [Ref](https://forum.openwrt.org/t/support-for-tp-link-archer-c7-v5-ru/28402)
