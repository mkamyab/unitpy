from unittest import TestCase
import timeit

import pint


class TestUnits(TestCase):
    def test_performance(self):
        runs = 10000

        # Without unit analysis
        timeit_base = timeit.timeit(
            '3.2 + 4.3 * 0.3048',
            number=runs
        )
        print(timeit_base)

        # OURS
        timeit_ours = timeit.timeit(
            # '3.2 * METER + 4.3 * foot',
            # '3.2 * METER / SECOND + 4.3 * foot / SECOND',
            '3.2 * METER / SECOND + 4.3 * foot / SECOND; 3.2 * METER / SECOND ** 2 + 4.3 * foot / minute ** 2',
            number=runs,
            setup='from src.registry import METER, SECOND;'
                  'from src.unit import Unit;'
                  'foot = Unit(0.3048, [(METER, 1)], "ft");'
                  'minute = Unit(60, [(SECOND, 1)], "ft")'
        )
        print(timeit_ours)

        # PINT
        timeit_pint = timeit.timeit(
            # '3.2 * meter + 4.3 * foot',
            '3.2 * meter / second + 4.3 * foot / second; 3.2 * meter / second ** 2 + 4.3 * foot / minute ** 2;',
            number=runs,
            setup='import pint;'
                  'ureg = pint.UnitRegistry();'
                  'meter = ureg.meter;'
                  'foot = ureg.foot;'
                  'second = ureg.second;'
                  'minute = ureg.minute;'
        )
        print(timeit_pint)

        comp_pint = timeit_pint / timeit_ours
        comp_base = timeit_ours / timeit_base
        print(f"Ours is {round(comp_pint, 2)} times faster than Pint.")
        print(f"Ours is {round(comp_base)} times slower than base.")

    def test_pint(self):
        ureg = pint.UnitRegistry()
        deg = ureg.deg
        angle = 3 * deg + 5
        print(angle.m_as(angle))