# 사용법

## 실행순서
```
python3 igmpreport_extract_from_pcap.py 0824-1005.pcap igmpreport.json 
python3 channel_analysis_from_igmpreport.py igmpreport.json channel.json
python3 remove_unknown_channel.py channel.json viewchannel.json
python3 program_analysis.py viewchannel.json program.json
```

# Changelog

## [160907] v0.0.2
- 출력 파일 이름 지정 가능
    - 입력: \*.pcap \*.json
    - 출력: \*.json
- [Bug Fix] Byte order 고려한 출력
- [New] 채널분석 모듈 기초 완성
    - 이름: channel\_analysis\_from\_igmpreport.py
    - 입력: \*igmp.json
    - 출력: \*channel.json

## [160902] v0.0.1
- 기초버전 완성
    - 이름: igmpreport\_extract\_from\_pcap.py
    - 입력: \*.pcap
    - 출력: igmp.json
