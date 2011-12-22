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
        texture = None
        tilesize = None
        leveldata = [  ]
        tile_defs = {   }
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
                except ValueError, IndexError:
                    warn("Expected an integer for @width; ignoring", line=ln)
                else:
                    info("Width: {}".format(width), line=ln)
            elif words[0] == '@height':
                try:
                    height = int(words[1])
                except ValueError, IndexError:
                    warn("Expected an integer for @height; ignoring", line=ln)
                else:
                    info("Height: {}".format(height), line=ln)
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
                        # COMMENT NEEDED TO EXPLAIN AWKWARD CODE
                        params['texture_location'] = params['texture']
                        del params['texture']
                    except KeyError:
                        pass
                    try:
                        tile_defs[char] = Tile(**params)
                    except TypeError:
                        warn("Unexpected parameter for @tt; ignoring", line=ln)
                    else:
                        info("Tiletype: char={} {}".format(char, params),
                             line=ln)
            elif words[0] == '@texture':
                try:
                    texture = pygame.image.load(words[1])
                except pygame.error as e:
                    warn("Couldn't load texture {}; ignoring".format(words[1]),
                         line=ln)
                else:
                    info("Texture: {}".format(texture), line=ln)
            elif words[0] == '@tilesize':
                try:
                    tilesize = int(words[1])
                except ValueError:
                    warn("Expected an integer for @tilesize; ignoring",
                         line=ln)
                else:
                    info("Tilesize: {}".format(tilesize), line=ln)
            elif words[0] == '@leveldata':
                info("Reading leveldata", line=ln)
                # Eat all of the leveldata lines
                try:
                    while not lines[ln+1].trim().startswith('@'):
                        ln += 1
                        leveldata.append(lines[ln].trim())
                except IndexError:
                    # We've reached the end of the file
                    pass
                info("Stopping reading leveldata", line=ln)
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

#    @staticmethod
#    def load_file(filename):
#        """Create a Level object from a level file"""
#        f = open(filename, "r")
#        lines = [line.strip() for line in f]
#        f.close()
#        # Strip leading and trailing whitespace, and trailing comments
#        for line in lines:
#            if line.find("#") == 0:
#                line = ""
#            if line.find("#") > 0:
#                line = line[:line.find("#")-1]
#        # Create a new Level object
#        l = Level()
#        # Store tiletypes for parsing
#        tiletypes = []
#        teximage = ""
#        l.tilesize = 1
#        i = 0
#        while i < len(lines):
#            if lines[i].startswith("@width "):
#                try:
#                    l.width = int(lines[i][7:])
#                except ValueError:
#                    print "Error reading field `width` while loading " + filename
#                else:
#                    print "Width: " + str(l.width)
#            elif lines[i].startswith("@height "):
#                try:
#                    l.height = int(lines[i][8:])
#                except ValueError:
#                    print "Error reading field `height` while loading " + filename
#                else:
#                    print "Height: " + str(l.height)
#            elif lines[i].startswith("@leveldata"):
#                i += 1
#                while i < len(lines) and not lines[i].startswith("@"):
#                    for char in lines[i]:
#                        l.tiles.append(ord(char))
#                    i += 1
#                i -= 1
#            elif lines[i].startswith("@texture "):
#                teximage = lines[i][9:]
#                print "Texture image: " + teximage
#            elif lines[i].startswith("@tilesize "):
#                try:
#                    l.tilesize = int(lines[i][10:])
#                except ValueError:
#                    print "Error reading field `tilesize` while loading " + filename
#                else:
#                    print "Tilesize: " + str(l.tilesize) + "px"
#            elif lines[i].startswith("@tt "):
#                args = lines[i][4:].split(' ')
#                print "TileType: " + str(args)
#                tiletypes.append(args)
#            i += 1
#
#        l.load_tiletypes(teximage, l.tilesize, tiletypes)
#        return l

#    def load_tiletypes(self, imagename, tsize, tiletypes):
#        image = None
#        try:
#            image = pygame.image.load(imagename)
#        except:
#            print "Unable to load spritesheet: " + imagename
#            return
#
#        for tt in tiletypes:
#            tt_id = 0
#            tt_fric = 0.0
#            tt_tex = None
#            for arg in tt:
#                if arg.startswith("char="):
#                    if len(arg) < 6:
#                        print "No char specified when trying to load TileType: " + str(tt)
#                    else:
#                        tt_id = ord(arg[5])
#                elif arg.startswith("friction="):
#                    try:
#                        tt_fric = float(arg[9:])
#                    except:
#                        print "Invalid friction value `" + arg[9:] + "` passed for TileType: " + str(tt)
#                elif arg.startswith("texture="):
#                    arg = arg[8:] # Remove "texture=" from the parser
#                    arg = arg.strip("()")
#                    x,y = 0,0
#                    try:
#                        x,y = arg.split(',')
#                        x,y = int(x), int(y)
#                    except:
#                        print "Invalid texture definition: " + arg
#                    tt_tex = image.subsurface(pygame.Rect(x, y, tsize, tsize))
#                    self.tiletypes[tt_id] = TileType(tt_id, tt_fric, tt_tex)
#        return # To be implemented

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
