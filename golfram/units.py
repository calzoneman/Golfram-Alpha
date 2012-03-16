px = 1/187. # m

class Unit:

    __slots__ = ('conversions', 'value', 'unit_name')

    def __init__(self, name, **conversions):
        self.unit_name = name
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
            return quantity.value
        elif quantity.unit_name in self.conversions:
            return quantity.value / self.conversions[quantity.unit_name]
        elif self.unit_name in quantity.conversions:
            return quantity.value * quantity.conversions[self.unit_name]
        else:
            raise ValueError("No conversion info for {0} to {1}".format(
                    quantity.unit_name, self.unit_name))

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

px = Unit('px')
m = Unit('m', px=187)

