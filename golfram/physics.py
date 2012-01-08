from golfram.util import error, info, warn

class God:

    def __init__(self, level, tracked_objects=None):
        if not tracked_objects:
            tracked_objects = []
        self.level = level
        self.tracked_objects = tracked_objects

    def tick(self, dt=1/60.0):
        for object in self.tracked_objects:
            tile = self.level.tile_at_point(object.position)
            # Calculate new velocity
            F = tile.force_on_object(object)
            m = obj.mass
            dv = F * dt / m
            object.velocity += dv
            # Move the object
            v = object.velocity
            dr = v * dt
            object.position += dr


if __name__ == '__main__':
    import doctest
    doctest.testmod()
