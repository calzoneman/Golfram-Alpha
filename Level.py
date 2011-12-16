from Tile import *

def Level:
    
    global DEFAULT_TYPEID
    DEFAULT_TYPEID = 0

    def __init__(self, width=1, height=1):
        self.width = width
        self.height = height

        self.tilemap = {} # Dictionary {texid : pygame.Surface() with texture}
        self.tiletypes = {} # Dictionary {typeid : Tile() with that typeid}
        self.tiles = [] # Array of typeids
        self.tiles.append(DEFAULT_TYPEID)

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

    def load_from_file(self, filename):
        return # To be implemented

    def load_tiletypes(self):
        return # To be implemented

    def load_tilemap(self):
        return # To be implemented
