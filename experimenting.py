from random import choice
import sys

import pygame

from golfram.core import Level, Tile

sred = pygame.image.load('sprites/red.png')
sgreen = pygame.image.load('sprites/green.png')
sblue = pygame.image.load('sprites/blue.png')
red = Tile(texture=sred)
blue = Tile(texture=sblue)
green = Tile(texture=sgreen)

N = 6
choices = [red, green, blue]
tiles = [[choice(choices) for x in range(N)] for y in range(N)]

level = Level(tiles=tiles, tilesize=64, width=192, height=192)

ball = pygame.image.load('sprites/ball-12x12.png')
ball_position = [0, 0]

# setup pygame window
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Test stuff")
background = pygame.Surface(screen.get_size()).convert()

level.draw_on_surface(background)

# Event loop
pygame.time.set_timer(pygame.USEREVENT + 1, 30)
while True:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT + 1:
            ball_position[0] = (ball_position[0] + 1) % 640
            ball_position[1] = (ball_position[1] + 1) % 480
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, dest=(0, 0))
    screen.blit(ball, dest=ball_position)
    pygame.display.flip()
