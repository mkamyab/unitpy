from numbers import Number
from typing import Union

from src.unit import Unit, BaseUnit


class Measurement:

    def __init__(self, magnitude: Number, unit: Unit):
        # assignment and reducing
        self.magnitude = magnitude
        self.unit = unit

        # no reducing is required here since we want to keep
        # the provided unit

    def reduce(self):
        self.magnitude *= self.unit.factor
        self.unit._factor = 1

    def to(self, unit: Union[Unit, BaseUnit]) -> 'Measurement':
        if not self.unit.is_same_dimension(unit):
            raise Exception("The provided unit is not of the same dimension as the self unit!")

        new_magnitude = self.magnitude * self.unit.factor / unit.factor
        return Measurement(new_magnitude, unit)

    def magnitude_in(self, unit: Union[Unit, BaseUnit]) -> Number:
        if not self.unit.is_same_dimension(unit):
            raise Exception("The provided unit is not of the same dimension as the self unit!")

        return self.magnitude * self.unit.factor / unit.factor

    def m_in(self, unit: Union[Unit, BaseUnit]) -> Number:
        return self.magnitude_in(unit)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Measurement(self.magnitude * other, self.unit)

        if isinstance(other, (Unit, BaseUnit)):
            new_unit = self.unit * other

            if isinstance(new_unit, Number):
                return self.magnitude * new_unit

            return Measurement(self.magnitude, new_unit)

        if isinstance(other, Measurement):
            new_magnitude = self.magnitude * other.magnitude
            new_unit = self.unit * other.unit

            if isinstance(new_unit, Number):
                return self.magnitude * new_unit

            return Measurement(new_magnitude, new_unit)

        raise ValueError('other value if of wrong type')

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Number):
            return Measurement(self.magnitude / other, self.unit)

        if isinstance(other, (Unit, BaseUnit)):
            new_unit = self.unit / other

            if isinstance(new_unit, Number):
                return self.magnitude / new_unit

            return Measurement(self.magnitude, new_unit)

        if isinstance(other, Measurement):
            new_magnitude = self.magnitude / other.magnitude
            new_unit = self.unit / other.unit

            if isinstance(new_unit, Number):
                return self.magnitude * new_unit

            return Measurement(new_magnitude, new_unit)

        raise ValueError('other value if of wrong type')

    def __rtruediv__(self, other):
        return (self ** -1).__mul__(other)


    def __add__(self, other: 'Measurement') -> 'Measurement':
        if not self.unit.is_same_dimension(other.unit):
            raise Exception("Values are not of the same dimension!")

        other = other.to(self.unit)
        return Measurement(self.magnitude + other.magnitude, self.unit)

    def __sub__(self, other: 'Measurement') -> 'Measurement':
        if not self.unit.is_same_dimension(other.unit):
            raise Exception("Values are not of the same dimension!")

        other = other.to(self.unit)
        return Measurement(self.magnitude - other.magnitude, self.unit)

    def __pow__(self, p: Number) -> 'Measurement':
        return Measurement(
            magnitude=self.magnitude ** p,
            unit=self.unit ** p
        )

    def __str__(self):
        unit_str = str(self.unit)
        return f"{self.magnitude} x |{unit_str}|"
