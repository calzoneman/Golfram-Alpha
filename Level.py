import pygame
from pygame.locals import *
from TileType import *

class Level:

    DEFAULT_TYPEID = 0

    def __init__(self, width=1, height=1):
        self.width = width
        self.height = height

        self.tiletypes = {} # Dictionary {typeid : TileType() with that typeid}
        self.tiles = [] # The level data
        self.tilesize = 1 # The edge length of a tile, in pixels

    def add_row(self):
        self.tiles.append([Level.DEFAULT_TYPEID for a in range(self.width)])
        self.height += 1

    def add_rows(self, rows):
        for a in range(rows):
            self.add_row()

    def add_column(self):
        self.width += 1
        for j in range(len(self.tiles)):
            self.tiles[j].append(Level.DEFAULT_TYPEID)

    def add_columns(self, cols):
        for a in range(cols):    
            self.add_column()

    def get_at(self, xy): # Returns a TileType object
        if xy[0] >= self.width or xy[1] >= self.height or xy[0] < 0 or xy[1] < 0:
            return None 
        return self.tiletypes[tiles[xy[1]][xy[0]]]

    def set_at(self, xy, t): # t is the typeid, not a TileType object
        if xy[0] >= self.width or xy[1] >= self.height or xy[0] < 0 or xy[1] < 0:
            return
        self.tiles[xy[1]][xy[0]] = t

    def expand_and_set(self, xy, t):
        if xy[0] >= self.width:
            self.add_columns(xy[0] - self.width + 1)
        if xy[1] >= self.height:
            self.add_rows(xy[1] - self.height + 1)
        self.set_at(xy, t)

    def draw(self, x_offset, y_offset, width, height):
        surf = pygame.Surface((width * self.tilesize, height * self.tilesize), SRCALPHA)
        x = x_offset
        y = y_offset
        while y < y_offset + height and y < self.height:
            while x < x_offset + width and x < self.width:
                surf.blit(self.tiletypes[self.tiles[y * self.width + x]].get_texture(), ((x - x_offset) * self.tilesize, (y - y_offset) * self.tilesize))
                x += 1
            y += 1
            x = x_offset

        return surf

    def load_from_file(self, filename):
        try:
            handle = open(filename, "r")
        except:
            print "Failed to open " + filename + " for reading"
            return
        lines = [line.strip() for line in handle]
        handle.close()
        # Strip leading and trailing whitespace, and trailing comments
        for line in lines:
            if line.find("#") == 0:
                line = ""
            if line.find("#") > 0:
                line = line[:line.find("#")-1]
            line = line.strip()
        # Reset the tiles list
        self.tiles = []
        # Store tiletypes for parsing
        tiletypes = []
        teximage = ""
        self.tilesize = 1
        i = 0
        while i < len(lines):
            if lines[i].startswith("@width "):
                try:
                    self.width = int(lines[i][7:])
                    print "Width: " + str(self.width)
                except:
                    print "Error reading field `width` while loading " + filename
            elif lines[i].startswith("@height "):
                try:
                    self.height = int(lines[i][8:])
                    print "Height: " + str(self.height)
                except:
                    print "Error reading field `height` while loading " + filename
            elif lines[i].startswith("@leveldata"):
                i += 1
                while i < len(lines) and not lines[i].startswith("@"):
                    for char in lines[i]:
                        self.tiles.append(ord(char))
                    i += 1
                i -= 1
            elif lines[i].startswith("@texture "):
                teximage = lines[i][9:]
                print "Texture image: " + teximage
            elif lines[i].startswith("@tilesize "):
                try:
                    self.tilesize = int(lines[i][10:])
                    print "Tilesize: " + str(self.tilesize) + "px"
                except:
                    print "Error reading field `tilesize` while loading " + filename
            elif lines[i].startswith("@tt "):
                args = lines[i][4:].split(' ')
                print "TileType: " + str(args)
                tiletypes.append(args)
            i += 1

        self.load_tiletypes(teximage, self.tilesize, tiletypes)

    def load_tiletypes(self, imagename, tsize, tiletypes):
        image = None
        try:
            image = pygame.image.load(imagename)
        except:
            print "Unable to load spritesheet: " + imagename
            return

        for tt in tiletypes:
            tt_id = 0
            tt_fric = 0.0
            tt_tex = None
            for arg in tt:
                if arg.startswith("char="):
                    if len(arg) < 6:
                        print "No char specified when trying to load TileType: " + str(tt)
                    else:
                        tt_id = ord(arg[5])
                elif arg.startswith("friction="):
                    try:
                        tt_fric = float(arg[9:])
                    except:
                        print "Invalid friction value `" + arg[9:] + "` passed for TileType: " + str(tt)
                elif arg.startswith("texture="):
                    arg = arg[8:] # Remove "texture=" from the parser
                    arg = arg.strip("()")
                    x,y = 0,0
                    try:
                        x,y = arg.split(',')
                        x,y = int(x), int(y)
                    except:
                        print "Invalid texture definition: " + arg
                    tt_tex = image.subsurface(pygame.Rect(x, y, tsize, tsize))
                    self.tiletypes[tt_id] = TileType(tt_id, tt_fric, tt_tex)
        return # To be implemented

