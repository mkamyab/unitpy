class Dimension:
    def __init__(self, symbol: str):
        self.symbol = symbol


# Dimensions
DIMENSIONLESS = Dimension("")
TIME = Dimension("T")
LENGTH = Dimension("L")
MASS = Dimension("M")
ELECTRIC_CURRENT = Dimension("I")
MATERIAL_AMOUNT = Dimension("N")
LUMINOUS_INTENSITY = Dimension("C")
TEMPERATURE = Dimension("t")
