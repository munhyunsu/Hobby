#!/usr/bin/env python3

def get_hand(history = None):
    if history == None:
        return 'kawi'
    if history[1] == 'lose':
        return 'bo'
    elif history[1] == 'win':
        return 'bawi'
