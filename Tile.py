class Tile:
    
    def __init__(self, typeid, texid=0, friction=0.1):
        self.typeid = typeid
        self.friction = friction

    def get_id(self):
        return self.typeid

    def get_friction(self):
        return self.friction

    def set_id(self, newid):
        self.typeid = newid

    def set_friction(self, newfric):
        self.friction = newfric
