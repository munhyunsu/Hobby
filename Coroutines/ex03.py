#!/usr/bin/python3

# Implementation in pre-3.3 Python
def chain(*generators):
    for generator in generators:
        for item in generator:
            yield item

# Implementation in post-3.3 Python
def chain(*generators):
    for generator in generators:
        yield from generator
