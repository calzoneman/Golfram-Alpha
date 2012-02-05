import math

class Vector:
    """A simple two-dimensional vector"""

    __slots__ = ('x', 'y')

    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return 'Vector({}, {})'.format(self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    __hash__ = None

    def __bool__(self):
        return not self.x == 0 and not self.y == 0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, value):
        if isinstance(value, Vector):
            # Return the dot product
            return self.x * value.x + self.y * value.y
        else:
            return Vector(self.x * value, self.y * value)
    __rmul__ = __mul__

    def __truediv__(self, value):
        return Vector(self.x / value, self.y / value)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, value):
        self.x *= value
        self.y *= value

    def __itruediv__(self, value):
        self.x /= value
        self.y /= value

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __pos__(self):
        return self

    @property
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        """Return a unit vector in the direction of self"""
        return self / self.magnitude
