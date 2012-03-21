from golfram.units import px

class Canvas:
    """A wrapper for pygame's Surface to help with offsets and rendering

    Surfaces can be easily split into subsurfaces, which can then be passed
    to other objects to be drawn on and painlessly re-incorporated to the main
    Surface. This allows objects to draw themselves with no knowledge of
    offsets or position.

    """
    def __init__(self, surface, bounds=None):
        self.surface = surface
        self.bounds = bounds
        self.width = surface.get_width() * px
        self.height = surface.get_height() * px

    def add(self, entity):
        if self.bounds.contains(entity.position):
            destination = (px(entity.position.x), px(entity.position.y)
            self.surface.blit(entity.texture, destination)

    def blit(self, *args):
        self.surface.blit(*args)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
