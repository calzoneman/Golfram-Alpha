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
    >>> p = Point2(x, y)
    >>> l.tile_at_point(p) is t3
    True

"""
from euclid import Point2, Vector2
import pygame

from golfram.util import get_path, info, warn

class Level:

    DEFAULT_PIXELS_PER_METER = 187
    DEFAULT_TILESIZE = 32

    def __init__(self, tiles=None, tilesize=DEFAULT_TILESIZE, width=0,
                 height=0, pixels_per_meter=DEFAULT_PIXELS_PER_METER):
        if not tiles:
            tiles = []
        self._tiles = list(tiles) # The level data
        self.tilesize = int(tilesize) # The edge length of a tile, in pixels
        self.width = int(width)
        self.height = int(height)
        self.pixels_per_meter = int(pixels_per_meter)

    def tiles_to_px(self, tile_units):
        """Return the pixels equivalent of a dimension in tile units"""
        return tile_units * self.tilesize

    def tile_under_px(self, px_x, px_y):
        """Return the Tile underneath the position specified in pixels"""
        row =    int(px_y // self.tilesize)
        column = int(px_x // self.tilesize)
        return self.get_tile(row, column)

    def tile_at_point(self, point):
        """Return the tile at the given point.

        point is a Point2 instance, point.x and point.y are in meters.

        """
        row = int(point.y * self.pixels_per_meter // self.tilesize)
        column = int(point.x * self.pixels_per_meter // self.tilesize)
        return self.get_tile(row, column)

    def append_row(self, tile=None):
        """Append a row of the given tile to the level"""
        if not tile:
            tile = self._default_tile
        self._tiles.append([tile] * self.width)
        self.height += 1

    def append_column(self, tile=None):
        """Append a column of the given tile to the level"""
        if not tile:
            tile = self._default_tile
        for row in self._tiles:
            row.append(tile)
        self.width += 1

    def get_tile(self, row, column):
        """Return the tile at the given coordinates

        Returns None if an IndexError occurs

        Hint: You can use tuple unpacking when you call the function.
        coordinates = (x, y)
        level.get_tile(*coordinates)

        """
        try:
            return self._tiles[row][column]
        except IndexError:
            return None

    def set_tile(self, row, column, tile):
        """Set the tile at the given coordinates

        Returns True if the setting is successful, False if it is not.

        """
        try:
            self._tiles[row][column] = tile
        except IndexError:
            return False
        # Note: If you know of a good way to make sure 'tile' is actually
        # an instance of Tile(), please add a check for that
        else:
            return True

    def expand_and_set(self, xy, t):
        """ Deprecated

        Left here for reference when building future functions

        """
        if xy[0] >= self.width:
            self.add_columns(xy[0] - self.width + 1)
        if xy[1] >= self.height:
            self.add_rows(xy[1] - self.height + 1)
        self.set_at(xy, t)

    def draw(self, row_start=0, column_start=0, rows=None, columns=None):
        if not rows:
            rows = self.width - row_start
        if not columns:
            columns = self.height - column_start
        surface = pygame.Surface((self.tiles_to_px(rows), self.tiles_to_px(columns)), pygame.SRCALPHA)
        row = row_start
        column = column_start
        while row < row_start + rows and row < self.height:
            while column < column_start + columns and column < self.width:
                surface.blit(self.get_tile(row, column).texture,
                             (self.tiles_to_px(column - column_start), self.tiles_to_px(row - row_start)))
                column += 1
            row += 1
            column = column_start
        return surface

#    def draw(self, x_offset, y_offset, width, height):
#        surf = pygame.Surface((width * self.tilesize, height * self.tilesize), SRCALPHA)
#        x = x_offset
#        y = y_offset
#        while y < y_offset + height and y < self.height:
#            while x < x_offset + width and x < self.width:
#                surf.blit(self.tiletypes[self.tiles[y * self.width + x]].get_texture(), ((x - x_offset) * self.tilesize, (y - y_offset) * self.tilesize))
#                x += 1
#            y += 1
#            x = x_offset
#
#        return surf

    @staticmethod
    def load_file(filename):
        """Create a Level object from a level file"""
        width = None
        height = None
        tilesize = None
        leveldata = [ ]
        tile_defs = { }
        # Read in the file. Don't catch IO exceptions here... it's up to the
        # code that calls this to decide what to do.
        f = open(filename, 'r')
        lines = [None] + f.readlines()
        f.close()
        ln = 1
        while ln < len(lines):
            # Remove comments and split line into words based on whitespace
            words = lines[ln][:lines[ln].find('#')].split()
            if words[0] == '@width':
                try:
                    width = int(words[1])
                except (ValueError, IndexError):
                    warn("Expected an integer for @width; ignoring", line=ln,
                         file=filename)
                else:
                    info("Width: {}".format(width), line=ln, file=filename)
            elif words[0] == '@height':
                try:
                    height = int(words[1])
                except (ValueError, IndexError):
                    warn("Expected an integer for @height; ignoring", line=ln,
                         file=filename)
                else:
                    info("Height: {}".format(height), line=ln, file=filename)
            elif words[0] == '@leveldata':
                info("Reading leveldata", line=ln, file=filename)
                # Eat all of the leveldata lines
                try:
                    while not lines[ln+1].strip().startswith('@endleveldata'):
                        ln += 1
                        leveldata.append(\
                            lines[ln][:lines[ln].find('#')].strip())
                except IndexError:
                    # We've reached the end of the file
                    pass
                info("Stopping reading leveldata", line=ln, file=filename)
            elif words[0] == '@tiledefs':
                try:
                    info("Loading tile definitions from {}".format(words[1]))
                except IndexError:
                    warn("Expected a filename for @tiledefs", line=ln,
                         file=filename)
                else:
                    tilesize, tile_defs = Level.load_tiledefs(
                            get_path(words[1], 'tiledef'))
                    info("Loaded tile definitions", line=ln, file=filename)
            elif words[0] == '@endleveldata':
                pass
            else:
                warn("Unexpected line; ignoring", line=ln, file=filename)
            ln += 1
        # End parsing loop
        # Build the array of tiles
        tiles = []
        row = 0
        for line in leveldata:
            row = []
            for char in line:
                try:
                    row.append(tile_defs[char])
                except KeyError:
                    warn("Invalid character encountered in leveldata!")
                    # Append some sort of default or placeholder tile here
            tiles.append(row)
        return Level(tiles=tiles, tilesize=tilesize, width=width,
                     height=height)

    @staticmethod
    def load_tiledefs(filename):
        f = open(filename, 'r')
        lines = [None] + f.readlines()
        f.close()
        texture = None
        tilesize = None
        tile_defs = { }
        ln = 1
        while ln < len(lines):
            # Remove comments and split line into words based on whitespace
            words = lines[ln][:lines[ln].find('#')].split()
            if words[0] == '@tilesize':
                try:
                    tilesize = int(words[1])
                except ValueError:
                    warn("Expected an integer for @tilesize; ignoring",
                         line=ln, file=filename)
                else:
                    info("Tilesize: {}".format(tilesize), line=ln,
                         file=filename)
            elif words[0] == '@texture':
                try:
                    texture = pygame.image.load(get_path(words[1], "texture"))
                except pygame.error as e:
                    warn("Couldn't load texture {}; ignoring".format(words[1]),
                         line=ln, file=filename)
                else:
                    info("Texture: {}".format(texture), line=ln, file=filename)
            elif words[0] == '@tt':
                params = {}
                for word in words[1:]:
                    t = word.split('=')
                    params[t[0]] = t[1]
                try:
                    char = params['char']
                    del params['char']
                except KeyError:
                    warn("Expected a char= statement for @tt; ignoring",
                         line=ln, file=filename)
                else:
                    try:
                        # params['texture'] needs to be the actual image,
                        # not the coordinates specified by the @texture
                        # field in the tiledefs file
                        texture_args = params['texture'].strip("()").split(',')
                        x, y = int(texture_args[0]), int(texture_args[1])
                        params['texture_location'] = (x, y)
                        del params['texture']
                    except KeyError:
                        pass
                    except ValueError:
                        warn("Invalid position for tile texture; skipping",
                             line=ln, file=filename)
                    else:
                        try:
                            params['texture'] = texture.subsurface(
                                    pygame.Rect(params['texture_location'][0],
                                                params['texture_location'][1],
                                                tilesize, tilesize))
                        except AttributeError:
                            warn("Attempted to define tile texture without a" +
                                 " texture image specified; skipping", line=ln,
                                 file=filename)
                        except ValueError:
                            warn("Attempted to define tile texture without a" +
                                 " tilesize defined; skipping", line=ln,
                                 file=filename)
                        else:
                            del params['texture_location']
                            try:
                                tile_defs[char] = Tile(**params)
                            except TypeError:
                                warn("Unexpected parameter for @tt; ignoring",
                                     line=ln, file=filename)
                                warn(str(params), line=ln, file=filename)
                            else:
                                info("Tiletype: char={} {}".format(char, params),
                                     line=ln, file=filename)
            ln += 1
        return tilesize, tile_defs

    def draw_on_surface(self, surface):
        for y in range(len(self._tiles)):
            for x in range(len(self._tiles[y])):
                d = (x * self.tilesize, y * self.tilesize)
                surface.blit(self._tiles[y][x].texture, dest=d)


class Tile:

    def __init__(self, friction=0.1, texture=None):
        self.friction = float(friction)
        if texture:
            self.texture = texture
        else:
            self.texture = pygame.Surface((1,1))

    def force_on_object(self, object):
        """Calculate the frictional force applied by self to object.

        object must have the following properties:
         - mass, a scalar
         - velocity, a vector

        """
        direction = object.velocity.normalized() * -1
        force = object.mass * self.friction * direction
        return force


class BoostTile(Tile):

    def __init__(self, texture, friction, boost_force):
        self.texture = texture
        self.friction = friction
        self.boost_force = boost_force

    def force_on_object(self, object):
        frictional_force = super(BoostTile, self).force_on_object(object)
        # Should the boost force depend on the object's mass? For now... no.
        return frictional_force + self.boost_force


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
            position = Point2(0, 0)
        self.position = position
        self.mass = float(mass)
        self.diameter = float(diameter)
        self.velocity = Vector2(0, 0)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
