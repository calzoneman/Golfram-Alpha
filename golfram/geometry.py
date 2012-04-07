import math

class Circle:

    __slots__ = ('center', 'radius')

    def __init__(self, radius, center=None):
        if center:
            self.center = center
        else:
            self.center = Vector(0, 0)
        self.radius = radius


class Rectangle:
    """A simple two-dimensional rectangle"""

    __slots__ = ('height', 'nw', 'se', 'width')

    def __init__(self, nw=None, se=None, width=None, height=None):
        """Create a Rectangle

        offset is a Vector describing the position of the rectangle's top left
        corner relative to the origin.

        """
        if width and height:
            if se and not nw:
                self.se = se
                self.nw = Vector(self.se.x - width, self.se.y - height)
            else:
                if nw:
                    self.nw = nw
                else:
                    self.nw = Vector(0, 0)
                self.se = Vector(self.nw.x + width, self.nw.y + height)
        elif nw and se:
            self.nw = nw
            self.se = se
            self.width = self.se.x - self.nw.x
            self.height = self.se.y - self.nw.y
        else:
            raise ValueError("Invalid argument combination")

    def __repr__(self):
        return 'Rectangle({0!r}, {1!r})'.format(self.nw, self.se)

    def __str__(self):
        return self.__repr__()

    def contains(self, point):
        return (point.x >= self.nw.x and point.x <= self.sw.x and
                point.y >= self.nw.y and point.y <= self.sw.y)

    def is_touching(self, rectangle):
        raise NotImplemented()


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
