from random import choice
import sys

import pygame

from golfram.ball import Ball
from golfram.geometry import Vector
from golfram.level import BoostTile, Level, Tile
from golfram.physics import God

# Load tile textures and make tiles
class Red(Tile):
    texture = pygame.image.load('sprites/red.png')

class Green(Tile):
    texture = pygame.image.load('sprites/green.png')

class Blue(Tile):
    texture = pygame.image.load('sprites/blue.png')

class Boost(BoostTile):
    boost_velocity = Vector(-2, 0)
    texture_active = pygame.image.load('sprites/boost_active.png')
    texture_inactive = pygame.image.load('sprites/boost_inactive.png')

while True:
    # Create a level of 6x6 random tiles
    N = 8
    choices = [Boost] + [Red] * 2 + [Green] * 2 + [Blue] * 2
    class RandomLevel(Level):
        tiles = [[choice(choices)() for x in range(N)] for y in range(N)]
        width = 64 * N
        height = 64 * N
    level = RandomLevel()

    # Load the ball texture
    ball = Ball(sprite=pygame.image.load('sprites/ball-12x12.png'))

    # setup pygame window
    pygame.init()
    screen = pygame.display.set_mode((level.width, level.height))
    pygame.display.set_caption("Test stuff")
    background = pygame.Surface(screen.get_size()).convert()

    level.draw(background)

    # Make physics
    god = God(level)
    god.watch(ball)

    # Give the ball an initial velocity
    ball.velocity = Vector(2, 1.1)

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
        level.draw(background)
        screen.blit(background, dest=(0, 0))
        god.draw(screen)
        pygame.display.flip()

