"""The core classes for Golfram Alpha (Level, Tile, Ball, etc.)

Doctests:

Get a Tile based on its row/column:

    >>> t = Tile()
    >>> level = Level([[t,t,t]] * 3)
    >>> row, column = 0, 2
    >>> level.get_tile(row, column) is t
    True

Level.tile_at_point():

    >>> t1 = Tile()
    >>> t2 = Tile()
    >>> t3 = Tile()
    >>> l = Level([[t1],[t2],[t3]])
    >>> x = l.tilesize * 0.5 / l.pixels_per_meter
    >>> y = l.tilesize * 2.5 / l.pixels_per_meter
    >>> p = Vector(x, y)
    >>> l.tile_at_point(p) is t3
    True

"""
import pygame

from golfram.ball import Ball
from golfram.geometry import Vector
from golfram.util import get_path, info, warn

class Level:
    """Base level class

    Every Golfram level is defined by a subclass of Level. The simplest level
    would only define the grid of tiles and the solution condition.

    """
    # Actual levels (subclasses) will redefine these:
    ball = Ball
    pixels_per_meter = 187
    tilesize = 64
    tiles = None
    width = None
    height = None

    def __init__(self):
        # The idea here is to keep track of what things we need to redraw,
        # instead of redrawing everything every frame. I'm not sure what
        # to store here, though; the objects themselves is a possibility, or
        # maybe points or areas that have been soiled (but then we would have
        # to figure out all the objects that are drawn in those points/areas
        # which might be impossible).
        self._redraw_queue = []

    def tiles_to_px(self, tile_units):
        """Return the pixels equivalent of a dimension in tile units"""
        return tile_units * self.tilesize

    def tile_at_point(self, point):
        """Return the tile at the given point.

        point is a Vector instance, point.x and point.y are in meters.

        """
        row = int(point.y * self.pixels_per_meter // self.tilesize)
        column = int(point.x * self.pixels_per_meter // self.tilesize)
        return self.get_tile(row, column)

    def get_tile(self, row, column):
        """Return the tile at the given coordinates

        Returns None if an IndexError occurs

        Hint: You can use tuple unpacking when you call the function.
        coordinates = (x, y)
        level.get_tile(*coordinates)

        """
        # Don't allow negative indices (which *are* valid for lists)
        if row < 0 or column < 0:
            raise IndexError
        return self.tiles[row][column]

    # This is currently being used in experimenting.py
    def draw(self, surface):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                d = (x * self.tilesize, y * self.tilesize)
                surface.blit(self.tiles[y][x].texture, dest=d)


class Tile:

    friction = 0.4
    texture = None

    def acceleration_on_object(self, object):
        """Calculate the frictional acceleration applied by self to object.

        object must have the vector property 'velocity'.

        """
        direction = -object.velocity.normalize()
        friction = self.friction * direction
        return friction

    def draw(self):
        return self.texture

    def on_enter(self, object):
        pass

    def on_exit(self, object):
        pass


class BoostTile(Tile):

    boost_velocity = None
    friction = 5.0
    texture_active = None
    texture_inactive = None

    @property
    def texture(self):
        if self.active > 0:
            return self.texture_active
            self.active = 0 # A hack, for now
        else:
            return self.texture_inactive

    def __init__(self, *args):
        self.active = 0

    def acceleration_on_object(self, object):
        friction = Tile.acceleration_on_object(self, object)
        self.active += 1 # A hack, for now
        # This calculation is still wrong... the velocity should ramp toward
        # the target velocity
        velocity_projection = object.velocity.projection(self.boost_velocity)
        dv = self.boost_velocity - velocity_projection
        object.velocity += dv / 60
        return friction

    def on_enter(self, object):
        self.active += 1

    def on_exit(self, object):
        self.active -= 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
