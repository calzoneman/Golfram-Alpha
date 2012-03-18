import math

class Rectangle:
    """A simple two-dimensional rectangle"""

    __slots__ = ('height', 'nw', 'se', 'width')

    def __init__(self, width=None, height=None, offset=None):
        """Create a Rectangle

        offset is a Vector describing the position of the rectangle's top left
        corner relative to the origin.

        """
        self.nw = nw
        self.se = se
        if width is not None and height is not None:
            self.width = float(width)
            self.height = float(height)

    def __repr__(self):
        return 'Rectangle({!r}, {}, {})'.format(self.corner, self.width,
                                              self.height)

    def __str__(self):
        return "{}x{} rectangle at {}".format(self.width, self.height,
                                              self.corner)

    def is_touching(self, rectangle):
        pass


class Surface:
    """A wrapper for pygame's Surface to help with offsets and rendering

    Surfaces can be easily split into subsurfaces, which can then be passed
    to other objects to be drawn on and painlessly re-incorporated to the main
    Surface. This allows objects to draw themselves with no knowledge of
    offsets or position.

    """
    pass


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
    __div__ = __truediv__ # Needed for Python 2.x

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __pos__(self):
        return Vector(self.x, self.y)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        return [self.x, self.y][key]

    @property
    def magnitude(self):
        """Calculate the magnitude of the vector

        >>> Vector(-12, 0).magnitude
        12.0
        >>> Vector(3, 4).magnitude
        5.0

        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        """Return a unit vector in the direction of the vector

        >>> Vector(-12, 0).normalize()
        Vector(-1.0, 0.0)
        >>> Vector(2, -7).normalize().magnitude
        1.0
        """
        return self / self.magnitude

    def project(self, other):
        """Calculates the vector projection onto other"""
        joseph = other.normalize()
        return self * joseph * joseph


if __name__ == '__main__':
    import doctest
    doctest.testmod()
