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

sleep_time = 60 * sleep_min

vol_level = (end_vol - start_vol) / duration_min

print 'I sleep for ' + str(sleep_time) + ' Seconds'
time.sleep(sleep_time)

print 'Stop the Music'
player_iface.Stop()
