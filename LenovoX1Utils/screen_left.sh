#!/bin/bash

xrandr --output eDP1 --rotate left
xinput set-prop "Wacom Co.,Ltd. Pen and multitouch sensor Finger touch" "Coordinate Transformation Matrix" 0 -1 1 1 0 0 0 0 1
