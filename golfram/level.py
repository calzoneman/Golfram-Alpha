"""

Doctests:

Get a Tile based on its row/column:

    >>> from golfram.tile import Tile
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
    >>> x = m(l.tilesize * 0.5 * px)
    >>> y = m(l.tilesize * 2.5 * px)
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
        # This is a mapping of 'event_name' to a list of functions that should
        # be called when said event occurs.
        self._events = {}
        # This is a list of tuples of the level's entities and whether they
        # need to be physicsed.
        self._entities = []

    def add_entity(self, entity, physics=True):
        self._entities.append((entity, physics))

    def draw(self, canvas):
        # Draw all tiles for now. Later, only draw tiles from the _redraw_queue
        for row in range(len(self.tiles)):
            for column in range(len(self.tiles[row])):
                destination = (column * self.tilesize, row * self.tilesize)
                canvas.blit(self.tiles[row][column].texture, destination)
        # Draw all entities
        for entity in self._entities:
            canvas.add(entity)

    def get_tile(self, row, column):
        """Return the tile at the given coordinates"""
        # Don't allow negative indices (which *are* valid for lists)
        if row < 0 or column < 0:
            raise IndexError()
        return self.tiles[row][column]

    def tick(self, dt):
        for entity, physics in self._entities:
            if physics:
                tile = self.tile_at_point(entity.position)
                # Calculate new velocity
                a = tile.acceleration_on_object(entity)
                dv = a * dt
                entity.velocity += dv
                # Move the entity
                v = entity.velocity
                dr = 0.5 * a * dt**2 + v * dt
                entity.position += dr
                # If the entity moved onto a new tile, issue the appropriate
                # events, and mark the tiles to be redrawn.
                self._redraw_queue.append(tile)
                new_tile = self.tile_at_point(entity.position)
                if new_tile is not tile:
                    tile.exit_entity(entity)
                    new_tile.enter_entity(entity)
                    self._redraw_queue.append(new_tile)

    def tiles_to_px(self, tile_units):
        """Return the pixels equivalent of a dimension in tile units"""
        return tile_units * self.tilesize

    def tile_at_point(self, point):
        """Return the tile at the given point.

        point is a Vector instance, point.x and point.y are in meters.

        """
        row = int(px(point.y) // self.tilesize)
        column = int(px(point.x) // self.tilesize)
        return self.get_tile(row, column)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
