from golfram.core import Level, Tile, Ball
from golfram.util import error, info, warn

class God:

    def __init__(self, level, tracked_objects=None):
        if not tracked_objects:
            tracked_objects = []
        self.level = level
        self.tracked_objects = tracked_objects
        self.gravity_constant = self.level.tiles_to_px(4)

    def tick(self, dt=1/60.0):
        for obj in self.tracked_objects:
            # Calculate position
            obj.position[0] += obj.velocity[0] * dt \
                + obj.acceleration[0] * dt**2
            obj.position[1] += obj.velocity[1] * dt \
                + obj.acceleration[1] * dt**2
            # Calculate velocity
            obj.velocity[0] += obj.acceleration[0] * dt
            obj.velocity[1] += obj.acceleration[1] * dt

            # Reset the acceleration and apply friction for the next frame
            obj.acceleration = [0, 0]
            if int(obj.velocity[0]) is not 0 \
            and int(obj.velocity[1]) is not 0:
                mu = self.level.tile_under_px(*obj.position).friction

                # Resolve direction
                dir_x = -1 if obj.velocity[0] > 0 else 1
                dir_y = -1 if obj.velocity[1] > 0 else 1

                fric_x = dir_x * mu * obj.mass * self.gravity_constant
                fric_y = dir_y * mu * obj.mass * self.gravity_constant
                obj.apply_force([fric_x, fric_y])
