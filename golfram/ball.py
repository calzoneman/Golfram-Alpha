import pygame

from golfram.geometry import Circle, Rectangle, Vector

class GolfBall:

    diameter = 0.0427
    mass = 0.0459
    shape = Circle(diameter=diameter)
    sprite = pygame.image.load('sprites/ball-12x12.png')

    def __init__(self, position=None, velocity=None):
        if not position:
            position = Vector(0, 0)
        if not velocity:
            velocity = Vector(0, 0)
        self.position = position
        self.velocity = Vector(0, 0)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
