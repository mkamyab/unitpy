import abc
import copy
from numbers import Number
from typing import List, Union

from src.dimension import Dimension, DIMENSIONLESS


class Base(abc.ABC):
    _factor = 1

    @property
    @abc.abstractmethod
    def constituent_units(self) -> List:
        return NotImplemented

    @property
    @abc.abstractmethod
    def factor(self) -> Number:
        return NotImplemented

    @property
    @abc.abstractmethod
    def dimension(self) -> List:
        return NotImplemented

    def is_same_dimension(self, other: Union['Unit', 'BaseUnit']) -> bool:
        """
        To determine if the other unit and this one are of the same dimension.
        The requirement is that the units of self and other need to be already
        reduced and sorted.

        Args:
            other (Union['Unit', 'BaseUnit']): 

        Returns:
            bool: if self and other are of the same dimension
        """
        if len(self.constituent_units) != len(other.constituent_units):
            return False

        for index, [unit, power] in enumerate(self.constituent_units):
            [unit2, power2] = other.constituent_units[index]

            if unit != unit2 or power != power2:
                return False

        return True

    def is_unit_empty(self) -> bool:
        if self.constituent_units:
            return False
        return True


class Unit(Base):
    """
    The factor is the division of this Unit by its Constituent Units.
    """
    def __init__(self, factor: Number = None, constituent_units: List[List] = None, symbol: str = None):
        super(Unit, self).__init__()

        self.symbol = symbol

        self._factor = factor
        self._constituent_units = constituent_units

        # the unit will be reduced to its base unit once
        self._reduce_unit()

    @property
    def factor(self):
        return self._factor

    @property
    def constituent_units(self):
        return self._constituent_units

    @property
    def dimension(self):
        dimension_constituents = [
            [base_unit.dimension, power]
            for [base_unit, power] in self._constituent_units
        ]
        return dimension_constituents

    def _reduce_unit(self):
        # convert each unit to their base unit
        index = 0
        while index < len(self._constituent_units):
            [unit, power] = self._constituent_units[index]

            if isinstance(unit, BaseUnit):
                index += 1
                continue

            self._factor *= unit.factor ** power
            new_constituents = [
                [_unit, _power * power]
                for [_unit, _power] in unit._constituent_units
            ]
            self._constituent_units = [
                *self._constituent_units[:index],
                *new_constituents,
                *self._constituent_units[index + 1:]
            ]

        # mix similar base units
        index1 = 0
        while index1 < len(self._constituent_units) - 1:
            [unit1, power1] = self._constituent_units[index1]

            for index2_partial, (unit2, power2) in enumerate(self._constituent_units[index1 + 1:]):
                if unit1 != unit2:
                    continue

                index2 = index2_partial + (index1 + 1)

                self._constituent_units[index1][-1] = power1 + power2
                del self._constituent_units[index2]
                index1 -= 1
                break

            index1 += 1

        # trim the units; e.g. remove constituent units with power of 0
        self._constituent_units = [
            [unit, power]
            for [unit, power] in self._constituent_units
            if power != 0
        ]

        self._sort_units()

    def _sort_units(self):
        """
        To sort the units based on their name.
        This should be used after the reduction.
        """
        self._constituent_units.sort(key=lambda x: x[0].__class__.__name__)

    def __mul__(self, other: Union['Unit', 'BaseUnit', Number]):

        if isinstance(other, (Unit, BaseUnit)):
            factor = self.factor * other.factor

            constituent_units = [
                *self.constituent_units,
                *other.constituent_units
            ]

            new_unit = Unit(
                factor=factor,
                constituent_units=constituent_units
            )

            if new_unit.is_unit_empty():
                return factor

            return new_unit

        if isinstance(other, Number):
            from src.measurement import Measurement
            new_measure = Measurement(other, self)
            return new_measure

        raise ValueError(f"other is not of valid type")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other: Union['Unit', 'BaseUnit', Number]):  # TODO check canceling units
        if isinstance(other, (Unit, BaseUnit)):
            factor = self.factor / other.factor

            constituent_units = []
            constituent_units.extend(self.constituent_units)
            constituent_units.extend([[unit, -1 * power] for [unit, power] in other.constituent_units])

            new_unit = Unit(
                factor=factor,
                constituent_units=constituent_units
            )

            if new_unit.is_unit_empty():
                return factor

            return new_unit

        if isinstance(other, Number):
            from src.measurement import Measurement
            new_measure = Measurement(1 / other, self)
            return new_measure

        raise ValueError(f"other is not of valid type")

    def __rtruediv__(self, other):
        return (self ** -1).__mul__(other)

    def __pow__(self, p: Number) -> 'Unit':
        new_unit = Unit(
            factor=self._factor ** p,
            constituent_units=[
                [unit,  power * p]
                for (unit, power) in self.constituent_units
            ]
        )
        return new_unit

    def __str__(self):
        constituent_units_str = ", ".join([f"({str(each[0])}, {each[1]})" for each in self.constituent_units])
        return f"{self.factor} x [{constituent_units_str}]"


class BaseUnit(Base):
    def __init__(self, symbol: str, dimension: Dimension):
        super(BaseUnit, self).__init__()
        self.symbol = symbol

        self._dimension = dimension

    @property
    def factor(self):
        return 1

    @property
    def constituent_units(self):
        return [[self, 1]]

    @property
    def dimension(self):
        return self._dimension

    def __mul__(self, other):
        return self.to_unit().__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.to_unit().__truediv__(other)

    def __pow__(self, p: Number) -> 'Unit':
        return Unit(
            factor=1,
            constituent_units=[[self, p]]
        )

    def to_unit(self) -> Unit:
        return Unit(
            factor=1,
            constituent_units=[[self, 1]]
        )

    def __str__(self):
        return f"{self.symbol}"

    def __repr__(self):
        return f"{self.symbol}'{id(self)}'"

    # def __eq__(self, other):
    #     if not isinstance(other, BaseUnit):
    #         return None
    #
    #     if id(self) == id(other):
    #         return True
    #
    #     return False


class UnitlessUnit(BaseUnit):
    def __init__(self, symbol: str):
        super(UnitlessUnit, self).__init__(symbol, DIMENSIONLESS)

    # @property
    # def factor(self):
    #     return 1

    @property
    def constituent_units(self):
        return [[self, 1]]

    # @property
    # def dimension(self):
    #     return self._dimension

    # def __mul__(self, other):
    #     return self.to_unit().__mul__(other)
    #
    # def __rmul__(self, other):
    #     return self.__mul__(other)
    #
    # def __truediv__(self, other):
    #     return self.to_unit().__truediv__(other)
    #
    # def __pow__(self, p: Number) -> 'Unit':
    #     return Unit(
    #         factor=1,
    #         constituent_units=[[self, p]]
    #     )

    # def to_unit(self) -> Unit:
    #     return Unit(
    #         factor=1,
    #         constituent_units=[[self, 1]]
    #     )

    # def __str__(self):
    #     return f"{self.symbol}"