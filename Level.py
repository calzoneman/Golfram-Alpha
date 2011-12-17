import pygame
from pygame.locals import *
from Tile import *

class Level:
    
    global DEFAULT_TYPEID
    DEFAULT_TYPEID = 0

    def __init__(self, width=1, height=1):
        self.width = width
        self.height = height

        self.tilemap = {} # Dictionary {typeid : pygame.Surface()}
        self.tiletypes = {} # Dictionary {typeid : Tile() with that typeid}

        self.tiles = [] # Array of typeids

        self.tilesize = 1 # The edge length of a tile, in pixels

    def add_row(self):
        self.tiles.append([DEFAULT_TYPEID for a in range(self.width)])
        self.height += 1
    
    def add_rows(self, rows):
        for a in range(rows):
            self.add_row()

    def add_column(self):
        self.width += 1
        for j in range(len(self.tiles)):
            self.tiles[j].append(DEFAULT_TYPEID)

    def add_columns(self, cols):
        for a in range(cols):    
            self.add_column()

    def get_at(self, xy): # Returns a Tile object
        if xy[0] >= self.width or xy[1] >= self.height or xy[0] < 0 or xy[1] < 0:
            return None 
        return self.tiletypes[tiles[xy[1]][xy[0]]]

    def set_at(self, xy, t): # t is the typeid, not a Tile object
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
        surf = pygame.Surface(width * self.tilesize, height * self.tilesize, SRCALPHA)
        x = x_offset
        y = y_offset
        while y < y_offset + height and y < self.height:
            while x < x_offset + width and x < self.width:
                surf.blit(self.tilemap[self.tiles[y * self.width + x]], (x * self.tilesize, y * self.tilesize))
                x += 1
            y += 1
        
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
                    print "Error reading field `height` while loading" + filename
            elif lines[i].startswith("@leveldata"):
                i += 1
                while i < len(lines) and not lines[i].startswith("@"):
                    for char in lines[i]:
                        self.tiles.append(ord(char))
                    i += 1
            elif lines[i].startswith("@tt "):
                args = lines[i][4:].split(' ')
                print "TileType: " + str(args)

            i += 1


    def load_tiletypes(self):
        return # To be implemented

    def load_tilemap(self):
        return # To be implemented
