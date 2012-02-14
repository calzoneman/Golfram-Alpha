from golfram.util import error, info, warn

class God:

    def __init__(self, level):
        self.level = level
        self._objects = []

    def draw(self, surface):
        for object in self._objects:
            x = int(object.position.x * self.level.pixels_per_meter)
            y = int(object.position.y * self.level.pixels_per_meter)
            surface.blit(object.sprite, (x, y))

    def watch(self, object):
        self._objects.append(object)

    def tick(self, dt):
        for object in self._objects:
            tile = self.level.tile_at_point(object.position)
            if tile is None:
                raise IndexError("Ball out of bounds!")
            # Calculate new velocity
            a = tile.acceleration_on_object(object)
            dv = a * dt
            object.velocity += dv
            # Move the object
            v = object.velocity
            dr = 0.5 * a * dt**2 + v * dt
            object.position += dr


if __name__ == '__main__':
    import doctest
    doctest.testmod()
