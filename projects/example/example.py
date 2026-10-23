from classes import Bin, Shape

bins: list[Bin]
shapes: list[Shape]

# DIMENSIONS
WIDTH = 100
DEPTH = 50
X_WIDTH = 4
Y_WIDTH = 2

# BINS
bins: list[Bin] = [
    # LENGTH, WIDTH, COUNT
    Bin(120, 30, 2),
    Bin(80, 40, 2),
]

# SHAPES
shapes = [
    # NAME, LONGER_SIDE, SHORTER_SIDE
    Shape("Shelf", WIDTH, DEPTH),
    *(2 * Shape("Grid X", WIDTH, X_WIDTH)),
    *(15 * Shape("Grid Y", DEPTH, Y_WIDTH)),
]
