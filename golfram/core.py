"""The core classes for Golfram Alpha (Level, Tile, Ball, etc.)

Doctests:
>>> t = Tile(size=1)
>>> level = Level([[t,t,t]] * 3)
>>> coordinates = (3, 7)
>>> level.get_tile(**coordinates) is t
True

"""
import pygame
from pygame.locals import *

from golfram.util import warn, info

class Level:

    def __init__(self, tiles=None, *, width=1, height=1):
        self.width = width
        self.height = height

        self.tiletypes = {} # Dictionary {typeid : TileType() with that typeid}
        self._tiles = [] # The level data
        self.tilesize = 1 # The edge length of a tile, in pixels

    def px(self, tile_units):
        """Return the pixels equivalent of a dimension in tile units"""
        return tile_units * self.tilesize

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
        level.get_tile(**coordinates)

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

    def draw(self, row_start, column_start, rows, columns):
        surface = pygame.Surface((self.px(rows), self.px(columns)), SRCALPHA)
        row = row_start
        column = column_start
        while row < row_start + rows and row < self.rows:
            while column < column_start + columns and column < self.columns:
                surface.blit(self.get_tile(row, column).texture,
                             (px(column - column_start), px(row - row_start)))
                column += 1
            row += 1
            column = column_start
        return surf

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
        # Stairs
        width = None
        height = None
        leveldata = []
        # Read in the file. Don't catch IO exceptions here... it's up to the
        # code that calls this to decide what to do.
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        ln = 0
        while ln < len(lines):
            ln += 1
            # Remove comments and split line into words based on whitespace
            words = lines[ln][:lines[ln].find('#')].split()
            if words[0] == '@width':
                try:
                    width = int(words[1])
                except (ValueError, IndexError):
                    warn("Expected an integer for @width; ignoring", line=ln)
                else:
                    info("Width: {}".format(width), line=ln)
            elif words[0] == '@height':
                try:
                    height = int(words[1])
                except (ValueError, IndexError):
                    warn("Expected an integer for @height; ignoring", line=ln)
                else:
                    info("Height: {}".format(height), line=ln)

            elif words[0] == '@leveldata':
                info("Reading leveldata", line=ln)
                # Eat all of the leveldata lines
                try:
                    while not lines[ln+1].trim().startswith('@endleveldata'):
                        ln += 1
                        leveldata.append(\
                            lines[ln][:lines[ln].find('#')].trim())
                except IndexError:
                    # We've reached the end of the file
                    pass
                info("Stopping reading leveldata", line=ln)
            elif words[0] == '@tiledefs':
                try:
                    info("Attempting to load tile definitions from {}"\
                        .format(words[1]))
                except IndexError:
                    warn("Expected a filename for @tiledefs", line=ln)
                else:
                    tile_defs = Level.load_tiledefs(words[1])
            else:
                warn("Unexpected line; ignoring", line=ln)
        # End parsing loop
        # Build the array of tiles
        tiles = []
        row = 0
        for line in leveldata:
            column = 0
            for char in line:
                try:
                    tiles[row][column] = tile_defs[char]
                except KeyError:
                    warn("somethjing happen")
                column += 1
            row += 1
            column = 0
        return Level(tiles, width=width, height=height)

    @staticmethod
    def load_tiledefs(filename):
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()
        # Stairs 2.0
        texture = None
        tilesize = None
        tile_defs = {  }
        ln = 0
        while ln < len(lines):
            ln += 1
            # Remove comments and split line into words based on whitespace
            words = lines[ln][:lines[ln].find('#')].split()
            if words[0] == '@tilesize':
                try:
                    tilesize = int(words[1])
                except ValueError:
                    warn("Expected an integer for @tilesize; ignoring",
                         line=ln)
                else:
                    info("Tilesize: {}".format(tilesize), line=ln)
            elif words[0] == '@texture':
                try:
                    texture = pygame.image.load(words[1])
                except pygame.error as e:
                    warn("Couldn't load texture {}; ignoring"\
                        .format(words[1]), line=ln)
                else:
                    info("Texture: {}".format(texture), line=ln)
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
                         line=ln)
                else:
                    try:
                        # params['texture'] needs to be the actual image,
                        # not the coordinates specified by the @texture
                        # field in the tiledefs file
                        texture_args = params['texture']\
                            .strip("()")\
                            .split(',')
                        x, y = int(texture_args[0]), int(texture_args[1])

                        params['texture_location'] = (x, y)
                        del params['texture']
                    except KeyError:
                        pass
                    except ValueError:
                        warn("Invalid position specified for tile texture;\
                            skipping", line=ln)
                    else:
                        try:
                            params['texture'] = texture.subsurface(\
                            pygame.Rect(
                            params['texture_location'][0],\
                            params['texture_location'][1],\
                            tilesize,\
                            tilesize))
                        except AttributeError:
                            warn("Attempted to define tile texture without\
                            a texture image specified; skipping", line=ln)
                        except ValueError:
                            warn("Attempted to define tile texture without\
                            a tilesize defined; skipping", line=ln)
                        else:
                            try:
                                tile_defs[char] = Tile(**params)
                            except TypeError:
                                warn("Unexpected parameter for @tt;\
                                    ignoring", line=ln)
                            else:
                                info("Tiletype: char={} {}"\
                                    .format(char, params), line=ln)



class Tile:

    def __init__(self, friction=0.1, texture=None):
        try:
            self.friction = float(friction)
        except ValueError:
            warn("Invalid friction value: {}, defaulting to 0.1"\
                .format(friction))
            self.friction = 0.1
        if texture:
            self.texture = texture
        else:
            self.texture = pygame.Surface((1,1))
