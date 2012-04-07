class Tile(object):

    friction = 0.4
    texture = None

    def acceleration_on_object(self, object):
        """Calculate the frictional acceleration applied by self to object.

        object must have the vector property 'velocity'.

        """
        direction = -object.velocity.normalize()
        friction = self.friction * direction
        return friction

    def draw(self):
        return self.texture

    def on_enter(self, object):
        pass

    def on_exit(self, object):
        pass


class BoostTile(Tile):

    boost_velocity = None
    friction = 5.0
    texture_active = None
    texture_inactive = None

    @property
    def texture(self):
        if self.active > 0:
            return self.texture_active
        else:
            return self.texture_inactive

    def __init__(self, *args):
        self.active = 0

    def acceleration_on_object(self, object):
        friction = Tile.acceleration_on_object(self, object)
        # This calculation is still wrong... the velocity should ramp toward
        # the target velocity
        velocity_projection = object.velocity.project(self.boost_velocity)
        dv = self.boost_velocity - velocity_projection
        object.velocity += dv / 60
        return friction

    def on_enter(self, entity):
        self.active += 1

    def on_exit(self, entity):
        self.active -= 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
