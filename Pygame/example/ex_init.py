#!/usr/bin/env python3

import sys
import pygame


def main(argv):
    pygame.init()
    
    width = 800
    height = 600
    size = (width, height)
    speed = [2, 2]
    black = (0, 0, 0)

    screen = pygame.display.set_mode(size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
