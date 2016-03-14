#!/usr/bin/python
# -*- coding: utf8 -*-

import dbus
import time

session_bus = dbus.SessionBus()
player = session_bus.get_object('org.mpris.MediaPlayer2.clementine', '/org/mpris/MediaPlayer2')

#iface = dbus.Interface(player, 'org.freedesktop.DBus.Properties')

time.sleep(14400)
#time.sleep(1)

iface = dbus.Interface(player, 'org.mpris.MediaPlayer2.Player')
iface.Play()
