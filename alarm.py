#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import dbus
import time

##### Function Definition Area
def sleep(sleep_min):
	sleep_sec = 60 * sleep_min
	print 'I sleep for ' + str(sleep_sec) + ' Seconds'
	time.sleep(sleep_sec)
# End of def Sleep()


def connect_to_mpris2(music_player_name):
	session_bus = dbus.SessionBus()
	try:
		player = session_bus.get_object('org.mpris.MediaPlayer2.' + music_player_name, '/org/mpris/MediaPlayer2')
	except dbus.exceptions.DBusException:
		print 'We can\'t find ' + music_player_name + '. You need to launch ' + music_player_name
		sys.exit()
	prop_iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
	player_iface = dbus.Interface(player, 'org.mpris.MediaPlayer2.Player')

	print 'Success connect to DBus'

	return (prop_iface, player_iface)
# End of connect_to_mpris2()


def play_music(player_iface):
	print 'Play the Music'
	player_iface.Play()
# End of play_music()


def stop_music(player_iface):
	print 'Stop the Music'
	player_iface.Stop()
# End of stop_music()


def change_volume(prop_iface, start_vol, end_vol, duration_min):
	print 'Set volume(start) to ' + str(start_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', start_vol)

	if(duration_min > 0):
		duration_sec = 60 * duration_min
		vol_level = (end_vol - start_vol) / duration_sec
		current_vol = start_vol
		for vol_step in range(1, duration_sec+1):
			time.sleep(1)
			current_vol = current_vol + vol_level
			if(vol_step % 10 == 0):
				print 'Set volume(' + str(vol_step) + 'step) to ' + str(current_vol)
			prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', current_vol)

	print 'Set volume(end) to ' + str(end_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', end_vol)
# End of change_volume()
##### End of Function Definition Area


##### Main Area
def main():
	music_player = 'clementine'
	sleep_min = 60 * 5
	start_vol = 0.0
	end_vol = 1.0
	duration_min = 10

	(prop_iface, player_iface) = connect_to_mpris2(music_player)

	sleep(sleep_min)
	
	play_music(player_iface)

	change_volume(prop_iface, start_vol, end_vol, duration_min)

#	change_volume(prop_iface, end_vol, start_vol, duration_min)
	
#	stop_music(player_iface)
##### End of Main Area

if __name__ == '__main__':
	main()
