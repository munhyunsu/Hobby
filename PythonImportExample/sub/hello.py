#!/usr/bin/env python3

import sys
import os

import root_lib

def hello():
    print('It is sub hello', os.getcwd())
    root_lib.hello()

