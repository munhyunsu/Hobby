#!/usr/bin/python3
# -*- coding: utf-8 -*-
## Author: LuHa(munhyunsu@gmail.com)

def show_me_the_hand(records):
    hands = list()
    gawi_bawi_bo_list = ['gawi', 'bawi', 'bo']

    if(len(records) == 0):
        return 'bawi'

    hand = records[0]:
    if(hand[0] is 'gawi'):
        if(hand[1] == 1):
            return 'bawi'
        elif(hand[1] == 0):
            return 'bo'
        elif(hand[1] == -1):
            return 'gawi'
        else:
            return 'gawi'
    elif(hand[0] is 'bawi'):
        if(hand[1] == 1):
            return 'bo'
        elif(hand[1] == 0):
            return 'gawi'
        elif(hand[1] == -1):
            return 'bawi'
        else:
            return 'bawi'
    elif(hand[0] is 'bo'):
        if(hand[1] == 1):
            return 'gawi'
        elif(hand[1] == 0):
            return 'bawi'
        elif(hand[1] == -1):
            return 'bo'
        else:
            return 'bo'
    else:
        return 'gawi'

print(show_me_the_hand([('gawi', 1), ('bawi', 0), ('bo', -1)]))
