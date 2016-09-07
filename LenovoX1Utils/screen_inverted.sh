#!/bin/bash

xrandr --output eDP1 --rotate inverted
xinput set-prop "Wacom Co.,Ltd. Pen and multitouch sensor Finger touch" "Coordinate Transformation Matrix" -1 0 1 0 -1 1 0 0 1
