class XY(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def set_coordinates(self, o):
        if isinstance(o, list):
            self.x, self.y = o[0], o[1]
        elif isinstance(o, dict):
            self.x, self.y = o['x'], o['y']
        elif isinstance(o, XY):
            self.x, self.y = o.x, o.y
        else:
            raise ValueError(f"Cannot set coordinates from {o.__name__} - undefined.")

    def __rmul__(self, other):
        if not isinstance(other, int):
            raise ArithmeticError("Coordinate XY can by multiplied only by an int.")
        return XY(self.x*other, self.y*other)

    def __mul__(self, other):
        self.__rmul__(other)

    def __add__(self, other):
        if isinstance(other, XY):
            return XY(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return XY(self.x + other, self.y + other)
        elif isinstance(other, list) or isinstance(other, tuple):
            return XY(self.x + other[0], self.y + other[1])
        elif isinstance(other, dict):
            return XY(self.x + other['x'], self.y + other['y'])
        else:
            raise ArithmeticError(f"Adding for type {other.__name__} is not defined!")

    def __sub__(self, other):
        if isinstance(other, XY):
            return XY(self.x - other.x, self.y - other.y)
        elif isinstance(other, int):
            return XY(self.x - other, self.y - other)
        elif isinstance(other, list) or isinstance(other, tuple):
            return XY(self.x - other[0], self.y - other[1])
        elif isinstance(other, dict):
            return XY(self.x - other['x'], self.y - other['y'])
        else:
            raise ArithmeticError(f"Adding for type {other.__name__} is not defined!")

    def __str__(self):
        return f"[{self.x}, {self.y}]"
