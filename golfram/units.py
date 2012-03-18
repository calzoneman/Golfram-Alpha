px = 1/187. # m

class Unit:
    """Store conversion information for units of measure

    First, define a few Unit instances:
    >>> px = Unit('px', integral=True)
    >>> m = Unit('m', px=187)
    >>> m
    Unit('m')
    >>> 5*m
    5*m
    >>> 5*m + 3
    Traceback (most recent call last):
        ...
    AttributeError: 'int' object has no attribute 'unit_name'
    >>> 5*m + 3*px # doctest:+ELLIPSIS
    5.0160...*m
    >>> px(5*m + 3*px)
    937
    >>> m(64*px) # doctest:+ELLIPSIS
    0.3422...
    >>> m(5*m)
    5

    """
    __slots__ = ('conversions', 'value', 'unit_name')

    def __init__(self, name, integral=False, **conversions):
        self.unit_name = name
        self.integral = integral
        self.conversions = conversions
        self.value = None

    def __repr__(self):
        if self.value is None:
            return 'Unit({0!r})'.format(self.unit_name)
        else:
            return '{0}*{1}'.format(self.value, self.unit_name)

    def __call__(self, quantity):
        """Convert the quantity to this unit"""
        if quantity.unit_name == self.unit_name:
            result = quantity.value
        elif quantity.unit_name in self.conversions:
            result = quantity.value / float(self.conversions[quantity.unit_name])
        elif self.unit_name in quantity.conversions:
            result = quantity.value * quantity.conversions[self.unit_name]
        else:
            raise ValueError("No conversion info for {0} to {1}".format(
                                 quantity.unit_name, self.unit_name))
        if self.integral:
            result = int(result)
        return result

    def __add__(self, other):
        x = self.__copy__()
        x.value += x(other)
        return x

    def __sub__(self, other):
        x = self.__copy__()
        x.value -= x(other)
        return x

    def __mul__(self, other):
        x = self.__copy__()
        if x.value is None:
            x.value = other
        else:
            x.value *= other
        return x
    __rmul__ = __mul__

    def __truediv__(self, other):
        x = self.__copy__()
        x.value /= float(other)
        return x
    __div__ = __truediv__

    def __floordiv__(self, other):
        x = self.__copy__()
        x.value //= other
        return x

    def __copy__(self):
        x = Unit(self.unit_name, **self.conversions)
        x.value = self.value
        return x

px = Unit('px', integral=True)
m = Unit('m', px=187)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
