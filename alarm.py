#!/usr/bin/python
# -*- coding: utf8 -*-

##### Needed Variable
sleep_min = 240 # Sleep minute time
start_vol = 0 # Start Volume (0.0, 1.0)
end_vol = 1.0 # End Volume (0.0, 1.)
duration_min = 30 # Going Time from start_vol to end_vol
##### End Needed Variable

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


def play_with_change_volume(prop_iface, player_iface, start_vol, end_vol, duration_min):
	print 'Play the Music'
	player_iface.Play()
	
	vol_level = (end_vol - start_vol) / duration_min

	print 'Set volume to ' + str(start_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', start_vol)
	current_vol = start_vol
	for vol_step in range(1, duration_min+1):
		time.sleep(60)
		current_vol = current_vol + vol_level
		print 'Set volume(' + str(vol_step) + 'step) to ' + str(current_vol)
		prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', current_vol)
	print 'Set volume(last) to ' + str(current_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', end_vol)
# End of play_with_change_volume()


def stop_with_change_volume(prop_iface, player_iface, start_vol, end_vol, duration_min):
	vol_level = (end_vol - start_vol) / duration_min

	print 'Set volume to ' + str(start_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', start_vol)
	current_vol = start_vol
	for vol_step in range(1, duration_min+1):
		time.sleep(60)
		current_vol = current_vol + vol_level
		print 'Set volume(' + str(vol_step) + 'step) to ' + str(current_vol)
		prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', current_vol)
	print 'Set volume(last) to ' + str(current_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', end_vol)

	print 'Stop the Music'
	player_iface.Stop()
# End of stop_with_change_volume()


def play_music(player_iface):
	print 'Play the Music'
	player_iface.Play()
# End of play_music()


def stop_music(player_iface):
	print 'Stop the Music'
	player_iface.Stop()
# End of stop_music()


def change_volume(prop_iface, start_vol, end_vol, duration_min):
	vol_level = (end_vol - start_vol) / duration_min

	print 'Set volume to ' + str(start_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', start_vol)
	current_vol = start_vol
	for vol_step in range(1, duration_min+1):
		time.sleep(60)
		current_vol = current_vol + vol_level
		print 'Set volume(' + str(vol_step) + 'step) to ' + str(current_vol)
		prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', current_vol)
	print 'Set volume(last) to ' + str(current_vol)
	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', end_vol)
# End of change_volume()
##### End of Function Definition Area


##### Main Area
def main():
	music_player = 'clementine'
	sleep_min = 1
	start_vol = 0.0
	end_vol = 1.0
	duration = 1

	(prop_iface, player_iface) = connect_to_mpris2(music_player)

	sleep(sleep_min)

	#play_with_change_volume(prop_iface, player_iface, start_vol, end_vol, duration)
	
	play_music(player_iface)

	change_volume(prop_iface, start_vol, end_vol, duration)

##### End of Main Area

if __name__ == '__main__':
	main()





#session_bus = dbus.SessionBus()
#try:
#	player = session_bus.get_object('org.mpris.MediaPlayer2.clementine', '/org/mpris/MediaPlayer2')
#except dbus.exceptions.DBusException:
#	print 'Before run this programm, You need to launch clementine'
#	sys.exit()
#print 'Start this programm'
#
#prop_iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')
#player_iface = dbus.Interface(player, 'org.mpris.MediaPlayer2.Player')
##prop_iface.Get('org.mpris.MediaPlayer2.Player', 'Volume')
#
#sleep_time = 60 * sleep_min
#
#vol_level = (end_vol - start_vol) / duration_min
#
#print 'I sleep for ' + str(sleep_time) + ' Seconds'
#time.sleep(sleep_time)
#
#print 'Play the Music'
#prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', 0)
#player_iface.Play()
#
#print 'Set volume to ' + str(start_vol)
#cur_vol = start_vol
#prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', start_vol)
#for vol_step in range(1, duration_min+1):
#	time.sleep(60)
#	cur_vol = cur_vol + vol_level
#	print 'Set volume(' + str(vol_step) + 'step) to ' + str(cur_vol)
#	prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', cur_vol)
#print 'Set volume(last) to ' + str(cur_vol)
#prop_iface.Set('org.mpris.MediaPlayer2.Player', 'Volume', end_vol)
#
#print 'End this programm'


