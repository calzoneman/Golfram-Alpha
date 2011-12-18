from pygame import Surface

class TileType:
    
    def __init__(self, typeid, friction=0.1, texture=pygame.Surface((1,1))):
        self.typeid = typeid
        self.friction = friction
        self.texture = texture

    def get_id(self):
        return self.typeid

    def get_friction(self):
        return self.friction

    def get_texture(self):
        return self.texture

    def set_id(self, newid):
        self.typeid = newid

    def set_friction(self, newfric):
        self.friction = newfric

    def set_texture(self, newtex):
        self.texture = newtex
