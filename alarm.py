#!/usr/bin/python
# -*- coding: utf8 -*-

## Needed Variable
sleep_min = 1 # Sleep minute time
start_vol = 0 # Start Volume (0.0, 1.0)
end_vol = 1.0 # End Volume (0.0, 1.)
duration_min = 2 # Going Time from start_vol to end_vol
## End Needed Variable

import sys
import dbus
import time

session_bus = dbus.SessionBus()
try:
	player = session_bus.get_object('org.mpris.MediaPlayer2.clementine', '/org/mpris/MediaPlayer2')
except dbus.exceptions.DBusException:
	print 'Before run this programm, You need to launch clementine'
	sys.exit()
print 'Start this programm'

prop_iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
player_iface = dbus.Interface(player, 'org.mpris.MediaPlayer2.Player')
#prop_iface.Get('org.mpris.MediaPlayer2.Player', 'Volume')

sleep_time = 60 * sleep_min

vol_level = (end_vol - start_vol) / duration_min

print 'I sleep for ' + str(sleep_time) + ' Seconds'
time.sleep(sleep_time)

print 'Play the Music'
prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', 0)
player_iface.Play()

print 'Set volume to ' + str(start_vol)
cur_vol = start_vol
prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', start_vol)
for vol_step in range(1, duration_min+1):
	time.sleep(60)
	cur_vol = cur_vol + vol_level
	print 'Set volume(' + str(vol_step) + 'step) to ' + str(cur_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', cur_vol)
print 'Set volume(last) to ' + str(cur_vol)
prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', end_vol)

print 'End this programm'


