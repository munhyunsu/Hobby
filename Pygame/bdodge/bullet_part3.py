#!/usr/bin/env python3

import sys
import pygame

## pygame initionalize
pygame.init()
pygame.font.init()

## GLOBAL VARIABLES
# Version
VERSION = '0.1'
# Resolution
WIDTH = 800
HEIGHT = 600
# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 12)
DARK_ORANGE = (196, 121, 67)
# SCENE
STARTSCREEN = 'start_screen'
PLAYGAME = 'play_game'
GAMEOVER = 'game_over'
QUIT = 'quit'
# OPTIONS
FPS = 60
# PyGame
screen = None
font_title = pygame.font.Font(None, 65)
font_big = pygame.font.Font(None, 36)
font_default = pygame.font.Font(None, 28)


## MAIN
def main(argv):
    # display
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # window titlebar
    pygame.display.set_caption('Dodge ' + VERSION)
    # fps
    fps_clock = pygame.time.Clock()
    fps_clock.tick(FPS)
    # start_game
    main_loop()


## MAIN_LOOP: MAIN_SCREEN
def main_loop():
    user_action = STARTSCREEN
    while user_action != QUIT:
        if user_action == STARTSCREEN:
            user_action = start_screen()
        elif user_action == PLAYGAME:
            user_action = play_game()
        elif user_action == GAMEOVER:
            user_action = game_over()
    sys.exit(0)


## START_SCREEN
def start_screen():
    """
    https://www.pygame.org/docs/ref/key.html
    """
    global font_title
    global font_big
    global font_default
    global screen
    draw_text('BULLET DODGER', font_title, screen,
              WIDTH/2, HEIGHT/3, RED, YELLOW)
    draw_text('Press space when you are ready', font_big, screen,
              WIDTH/2, HEIGHT/2, GREEN, BLACK)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return PLAYGAME
            elif event.key == pygame.K_ESCAPE:
                return QUIT
        elif event.type == pygame.QUIT:
            return QUIT
    return STARTSCREEN


## PLAYGAME
def play_game():
    global font_default
    global screen
    screen.fill(BLACK)
    draw_text('PLAY GAME SCENE Press Any Key', font_default, screen,
              WIDTH/2, HEIGHT/2, WHITE, None)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return GAMEOVER
    return PLAYGAME


## GAMEOVER
def game_over():
    global font_default
    global screen
    screen.fill(BLACK)
    draw_text('GAME OVER SCENE Press Any Key', font_default, screen,
              WIDTH/2, HEIGHT/2, RED, WHITE)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return STARTSCREEN
    return GAMEOVER


### DRAW_TEXT
def draw_text(text, font, surface, x, y, main_color, back_color):
    """
    https://www.pygame.org/docs/ref/font.html
    https://www.pygame.org/docs/ref/surface.html
    """
    textobject = font.render(text, True, main_color, back_color)
    textrect = textobject.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobject, textrect)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
