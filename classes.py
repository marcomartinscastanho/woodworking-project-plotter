# -----------------------------
# DATA CLASSES
# -----------------------------
from config import PANEL_THICKNESS


class Shape:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width

    def __iter__(self):
        yield self.name
        yield self.length
        yield self.width

    def __repr__(self):
        return f"<{self.name}:\t{self.length} × {self.width} cm>"

    def __rmul__(self, n: int):
        for i in range(1, n + 1):
            yield Shape(f"{self.name} {i}", self.length, self.width)


class Bin:
    def __init__(self, length, width, count):
        self.length = length
        self.width = width
        self.count = count
        self.thickness = PANEL_THICKNESS

    def __iter__(self):
        yield self.length
        yield self.width
        yield self.count

    def __repr__(self):
        return f"<{self.count}:\t{self.length} × {self.width} cm>"
