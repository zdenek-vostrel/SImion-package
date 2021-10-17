from Simion.common import coordinate2D as C

class Base(object):
    def __init__(self, proportions={}):
        if hasattr(self, "proportions"):
            for key in proportions.keys():
                self.add_proportions(key, proportions[key])
        else:
            self.proportions = proportions

        if not hasattr(self, "scale"):
            self.scale = 1

        self.max_x = None
        self.max_y = None
        self.min_x = None
        self.min_y = None
        self.min_max_to_proportions(None, None, None, None)
        self.update_max_min()

        self.origin = None
        self.add_proportions("origin", None)

        # settings for gem generating
        self.potential = 1
        self.fill = True

    def set_scale(self, scale):
        self.scale = scale

    def get_proportions(self, scale=False):
        scale_factor = 1
        if scale is True:
            scale_factor = self.scale
        return {key: self.proportions[key] * scale_factor for key in self.proportions.keys()}

    def add_proportions(self, name, value, overwrite=False):
        if not overwrite and name in self.proportions.keys():
            print(f"Proportion {name} with value {value} was not set: it is already set to {self.proportions[name]}.")
            return
        self.proportions[name] = value

    def set_origin(self, origin):
        self.origin = self.to_xy(origin)
        self.add_proportions("origin", self.origin, overwrite=True)

    def get_origin(self, scale=False):
        if self.origin is None:
            return None
        if "origin" not in self.proportions.keys():
            self.add_proportions("origin", self.origin)
        return self.get_proportions(scale=scale)['origin']

    def min_max_to_proportions(self, max_x, max_y, min_x, min_y):
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.add_proportions("max_x", max_x)
        self.add_proportions("max_y", max_y)
        self.add_proportions("min_x", min_x)
        self.add_proportions("min_y", min_y)

    def update_max_min(self):
        self.check_correct_shape_settings()

    def check_correct_shape_settings(self):
        if None in [self.max_x, self.max_y, self.min_x, self.min_y]:
            raise ValueError('Shape settings are incorrect: min/max is None.')
        if self.origin is None or not isinstance(self.origin.x, int) or not isinstance(self.origin.y, int):
            raise ValueError('Origin not set correctly: must contain two int [x,y].')

    def get_max_x(self, scale=False):
        self.get("max_x", scale=scale)

    def get_max_y(self, scale=False):
        self.get("max_y", scale=scale)

    def get_min_x(self, scale=False):
        self.get("min_x", scale=scale)

    def get_min_y(self, scale=False):
        self.get("min_y", scale=scale)

    def get_max(self):
        return self.get_max_x(), self.get_max_y()

    def get_min(self):
        return self.get_min_x(), self.get_min_y()

    def get(self, name, scale=False):
        if name not in self.proportions.keys():
            raise ValueError(f"Key {name} is not in propotions!")
        return self.get_proportions(scale=scale)[name]

    def get_gem_input(self, scale=True):
        self.check_correct_shape_settings()

    def to_xy(self, o):
        c = C.XY(0, 0)
        c.set_coordinates(o)
        return c

