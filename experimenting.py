from random import choice
import sys

import pygame

from golfram.core import Ball, BoostTile, Level, Tile
from golfram.geometry import Vector
from golfram.physics import God

while True:
    # Load tile textures and make tiles
    sboost = pygame.image.load('sprites/boost_tile.png')
    sred = pygame.image.load('sprites/red.png')
    sgreen = pygame.image.load('sprites/green.png')
    sblue = pygame.image.load('sprites/blue.png')
    boost = BoostTile(texture=sboost, friction=0, boost=Vector(-4,0))
    red = Tile(texture=sred, friction=0.4)
    blue = Tile(texture=sblue, friction=0.4)
    green = Tile(texture=sgreen, friction=0.4)

    # Create a level of 6x6 random tiles
    N = 8
    choices = [boost, red, red, green, green, blue, blue]
    tiles = [[choice(choices) for x in range(N)] for y in range(N)]
    level = Level(tiles=tiles, tilesize=64, width=64*N, height=64*N)

    # Load the ball texture
    ball = Ball(sprite=pygame.image.load('sprites/ball-12x12.png'))

    # setup pygame window
    pygame.init()
    screen = pygame.display.set_mode((level.width, level.height))
    pygame.display.set_caption("Test stuff")
    background = pygame.Surface(screen.get_size()).convert()

    level.draw_on_surface(background)

    # Make physics
    god = God(level)
    god.watch(ball)

    # Give the ball an initial velocity
    ball.velocity = Vector(2, 1.0)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Move objects
        clock.tick(60)
        dt = clock.get_time() / 1000.0
        n = 10
        try:
            for i in range(n):
                god.tick(dt=dt/n)
        except IndexError:
            print("Ball out of bounds!")
            break
        #print ball.position
        # Stop if ball stops
        if ball.velocity.magnitude < 0.05:
            print("Ball stopped moving!")
            break
        # Update screen
        screen.blit(background, dest=(0, 0))
        god.draw(screen)
        pygame.display.flip()

