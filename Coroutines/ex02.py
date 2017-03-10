#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools

def averager():
    #print('a')
    sum = float((yield))
    #print('b')
    counter = itertools.count(start=1)
    #print('c')
    while True:
        #print('d', sum)
        sum += (yield sum / next(counter))
        #print('e', sum)


if __name__ == '__main__':
    #print('aa')
    avg = averager()
    #print('bb')
    print(avg.next())
    #print('cc')
    print(avg.send(10))
    #print('dd')
    print(avg.send(20))
    #print('ee')
    print(avg.send(30))
    #print('ff')
