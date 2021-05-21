from src.dimension import TIME, LENGTH, MASS, ELECTRIC_CURRENT, MATERIAL_AMOUNT, LUMINOUS_INTENSITY, TEMPERATURE

# Base Units
from src.unit import BaseUnit

SECOND = BaseUnit("s", TIME)
METER = BaseUnit("m", LENGTH)
KILOGRAM = BaseUnit("kg", MASS)
AMPERE = BaseUnit("A", ELECTRIC_CURRENT)
MOLE = BaseUnit("mol", MATERIAL_AMOUNT)
CANDELA = BaseUnit("cd", LUMINOUS_INTENSITY)
KELVIN = BaseUnit("K", TEMPERATURE)


# DIMENSION_UNIT_MAP = {
#     DIMENSIONLESS: UNITLESS, UNITLESS: DIMENSIONLESS,
#     TIME: SECOND, SECOND: TIME,
#     LENGTH: METER, METER: LENGTH,
#     MASS: KILOGRAM, KILOGRAM: MASS,
#     ELECTRIC_CURRENT: AMPERE, AMPERE: ELECTRIC_CURRENT,
#     MATERIAL_AMOUNT: MOLE, MOLE: MATERIAL_AMOUNT,
#     LUMINOUS_INTENSITY: CANDELA, CANDELA: LUMINOUS_INTENSITY,
#     TEMPERATURE: KELVIN, KELVIN: TEMPERATURE
# }


# TODO: Define Constants

