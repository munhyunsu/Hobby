# How to Monitor 802.11

## Prerequirements
```bash
apt-get install aircrack-ng
```

## Steps
1. Find channel for target WiFi
```bash
iwlist wlan0 scan
```

2. Set channel of device to that channel
```bash
ifconfig wlan0 down
iwconfig wlan0 channel 1
```

3. Change device mode from managed to monitor
```bash
airmon-ng start wlan0
```

4. Set channel of monitor device
```bash
ifconfig wlan0mon down
iwconfig wlan0mon channel 1
ifconfig wlan0mon promisc
```

5. Sniff, sniff!

## Useful resources and commands
- [Wireshark WiKi: WLAN Capture setup](https://wiki.wireshark.org/CaptureSetup/WLAN)
- [Wireshark WiKi: WiFi Capture](https://wiki.wireshark.org/Wi-Fi)
- Capture without beacon frames
```
 wlan[0] != 0x80
```
- Show only specific host
```
 wlan.addr == 08.00.08.15.ca.fe
```

