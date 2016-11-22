#!/bin/bash

python3 igmpreport_extract_from_pcap.py target.pcap igmpreport.json 
python3 channel_analysis_from_igmpreport.py igmpreport.json channel.json
python3 remove_unknown_channel.py channel.json viewchannel.json
python3 program_analysis.py viewchannel.json program.json
python3 iptv_diary.py program.json iptvdiary.json
