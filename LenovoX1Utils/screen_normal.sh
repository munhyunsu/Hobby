#!/bin/bash

xrandr --output eDP-1 --rotate normal
xinput set-prop "Wacom Co.,Ltd. Pen and multitouch sensor Finger touch" "Coordinate Transformation Matrix" 1 0 0 0 1 0 0 0 1
