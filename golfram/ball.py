import pygame

from golfram.geometry import Vector

class Ball:

    DEFAULT_MASS = 0.0459 # kg
    DEFAULT_DIAMETER = 0.0427 # m
    DEFAULT_SIZE = 8 # px

    def __init__(self, sprite=None, position=None, mass=DEFAULT_MASS,
                 diameter=DEFAULT_DIAMETER):
        if not sprite:
            sprite = pygame.Surface((DEFAULT_SIZE, DEFAULT_SIZE))
        self.sprite = sprite
        if not position:
            position = Vector(0, 0)
        self.position = position
        self.mass = float(mass)
        self.diameter = float(diameter)
        self.velocity = Vector(0, 0)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
