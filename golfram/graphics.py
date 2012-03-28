from golfram.units import px

class Canvas:
    """A wrapper for pygame's Surface to help with offsets and rendering

    Surfaces have a bounding rectangle which determines what part of the
    Surface is visible. Calls to draw at locations outside of the bounding
    rectangle could possibly be ignored.

    """
    def __init__(self, surface, bounds=None):
        self.surface = surface
        self.bounds = bounds
        self.width = surface.get_width() * px
        self.height = surface.get_height() * px

    def add_entity(self, entity):
        if self.bounds.contains(entity.position):
            destination = (px(entity.position.x), px(entity.position.y))
            self.surface.blit(entity.texture, destination)

    def scroll(self, bounds=None):
        self.bounds = bounds


if __name__ == '__main__':
    import doctest
    doctest.testmod()
