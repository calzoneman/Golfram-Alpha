from random import choice
import sys

import pygame

from golfram.ball import GolfBall
from golfram.geometry import Vector
from golfram.level import Level, LevelComplete
from golfram.tile import BoostTile, Tile

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

class RandomLevel(Level):

    def set_up(self):
        # Create a level of 6x6 random tiles
        N = 8
        choices = [Boost] + [Red] * 2 + [Green] * 2 + [Blue] * 2
        self.tiles = [[choice(choices)() for x in range(N)] for y in range(N)]
        # This is still wrong. We shouldn't have to define width and height at
        # all. Or at least not in pixels.
        self.width = 64 * N
        self.height = 64 * N
        # Spawn a new ball
        self.ball = self.ball_class()
        self.add_entity(self.ball)
        # Start it with some initial velocity, for experimenting!
        self.ball.velocity = Vector(2, 1.1)

    def is_complete(self):
        return self.ball.velocity.magnitude < 0.03

# setup pygame window
pygame.init()
screen = pygame.display.set_mode((64 * 8, 64 * 8))
pygame.display.set_caption("Test stuFf")

# Continuously generate test levels and shoot the ball across them
while True:
    level = RandomLevel(screen)
    clock = pygame.time.Clock()
    while True:
        # Draw
        level.draw(screen)
        pygame.display.flip()
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
                level.tick(dt=dt/n)
        except (IndexError, LevelComplete):
            break
    del level, clock
