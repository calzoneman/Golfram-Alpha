from Level import *
import pygame
from pygame.locals import *

class Game:

    def __init__(self, viewsize, level=None, players=[]):
        self.level = level
        self.players = players
        self.viewoffsetx = self.viewoffsety = 0
        self.viewsize = viewsize

    def load_level(self, levelname):
        self.level = Level.load_file(levelname)

    def add_player(self, ply):
        self.players.append(ply)

    def reset(self):
        self.level = None
        self.players = []
        self.viewoffsetx = self.viewoffsety = 0

    def tick(self):
        return

    def draw(self):
        return self.level.draw(self.viewoffsetx, self.viewoffsety, self.viewsize[0] / self.level.tilesize, self.viewsize[1] / self.level.tilesize)

    def scroll_down(self, amt=1):
        self.viewoffsety += amt

    def scroll_up(self, amt=1):
        if self.viewoffsety > amt:
            self.viewoffsety -= amt

    def scroll_left(self, amt=1):
        self.viewoffsetx += amt

    def scroll_right(self, amt=1):
        if self.viewoffsetx > amt:
            self.viewoffsetx -= amt


if __name__ == '__main__':
    import doctest
    doctest.testmod()
