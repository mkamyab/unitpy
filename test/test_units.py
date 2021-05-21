import math
from numbers import Number
from unittest import TestCase

from src.measurement import Measurement
from src.registry import SECOND, METER, KILOGRAM
from src.unit import Unit, UnitlessUnit


class TestUnits(TestCase):

    def test_unit_composition(self):

        minute = Unit(60, [[SECOND, 1]], "min")
        hour = Unit(60, [[minute, 1]], "hr")
        self.assertEqual(3600, hour.factor)

        foot = Unit(0.3048, [[METER, 1]], "ft")
        ft_per_hr1 = Unit(1, [[foot, 1], [hour, -1]])
        self.assertEqual(8.466666666666667e-05, ft_per_hr1.factor)

        newton = Unit(1, [[KILOGRAM, 1], [METER, 1], [SECOND, -2]], "N")
        lbf = Unit(4.44822, [[newton, 1]], "lbf")
        xlbf_2 = Unit(12, [[lbf, 2]])
        self.assertEqual(4.44822, lbf.factor)
        self.assertEqual(237.43993402080002, xlbf_2.factor)
        self.assertEqual(2, xlbf_2.constituent_units[0][1])  # add more of these

        radian = UnitlessUnit("rad")
        degree = Unit(math.pi / 180, [[radian, 1]], "deg")
        revolution = Unit(360, [[degree, 1]], "rev")
        self.assertEqual(2 * math.pi, revolution.factor)
        self.assertTrue(radian.is_same_dimension(revolution))

        moisture_content = UnitlessUnit("con")
        self.assertFalse(moisture_content.is_same_dimension(radian))

        radian_per_second = Unit(1, [[radian, 1], [SECOND, -1]])
        deg_per_minute = degree / minute
        self.assertEqual(math.pi / 180 / 60, deg_per_minute.factor)
        self.assertTrue(radian_per_second.is_same_dimension(deg_per_minute))

        degree2 = deg_per_minute * minute
        self.assertTrue(degree2.is_same_dimension(degree))
        self.assertTrue(degree2.is_same_dimension(radian))
        self.assertFalse(degree2.is_same_dimension(minute))

        ft_hr1 = Unit(1, [[foot, 1], [hour, 1]])
        ft_hr2 = foot * hour
        self.assertEqual(ft_hr1.factor, ft_hr2.factor)

        ft_per_hr2 = foot / hour
        self.assertEqual(ft_per_hr1.factor, ft_per_hr2.factor)

        ft_per_min_square1 = Unit(1, [[foot, 1], [minute, -2]], "ft/m2")
        ft_per_min_square2 = foot / minute ** 2
        self.assertEqual(ft_per_min_square1.factor, ft_per_min_square2.factor)
        self.assertEqual(1, ft_per_min_square2.constituent_units[0][1])  # power of meter
        self.assertEqual(-2, ft_per_min_square2.constituent_units[1][1])  # power of second

        METER_SECOND = METER * SECOND
        METER_SECOND_Squared = METER * SECOND ** 2
        self.assertTrue(isinstance(METER_SECOND_Squared, Unit))

        apple_amount = 0.1 * KILOGRAM
        self.assertTrue(isinstance(apple_amount, Measurement))

        METER_PER_SECOND_Squared = METER / SECOND ** 2
        apple_acceleration = 9.865 * METER_PER_SECOND_Squared

        apple_force = apple_amount * apple_acceleration
        self.assertTrue(0.9865, apple_force.magnitude)

        meter_per_second = METER / SECOND
        self.assertTrue(meter_per_second.is_same_dimension(ft_per_hr1))
        self.assertFalse(meter_per_second.is_same_dimension(ft_per_min_square2))

        duration = 1 * hour + 20 * minute
        self.assertAlmostEqual(1.3333333333333333, duration.magnitude, places=10)  # since keeping the hour magnitude
        self.assertEqual(80, duration.m_in(minute))

        print(f"duration: {duration.to(minute)}")

        apple_force_magnitude = apple_force / newton
        self.assertTrue(isinstance(apple_force_magnitude, Number))
        self.assertEqual(0.9865, apple_force_magnitude)


if __name__ == '__main__':
    tu = TestUnits()
    tu.test_unit_composition()
