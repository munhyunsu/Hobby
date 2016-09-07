#!/bin/bash

xrandr --output eDP1 --rotate right
xinput set-prop "Wacom Co.,Ltd. Pen and multitouch sensor Finger touch" "Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1
