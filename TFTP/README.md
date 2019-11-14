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
    - [Ref2](https://forum.openwrt.org/t/tp-link-archer-c7-v5-factory-bin-wont-load/22657)
  - But, above thing is not working (Maybe I fail image building). So, I tried compile whole [OpenWRT project](https://github.com/openwrt/openwrt).
    - [PATCH](http://lists.infradead.org/pipermail/openwrt-devel/2019-March/016296.html)
