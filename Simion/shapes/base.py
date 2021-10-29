from Simion.common import coordinate2D as C
import typing

class Base(object):
    def __init__(self, proportions={}):
        if hasattr(self, "proportions"):
            for key in proportions.keys():
                self.add_proportions(key, proportions[key])
        else:
            self.proportions = proportions

        if not hasattr(self, "scale"):
            self.scale = 1

        self.origin = None
        self.add_proportions("origin", None)

        self.max_x = None
        self.max_y = None
        self.min_x = None
        self.min_y = None
        self.min_max_to_proportions(None, None, None, None)
        # self.update_max_min()

        # settings for gem generating
        self.potential = 1
        self.fill = True

    def set_potential(self, value):
        if not isinstance(value, int):
            raise ValueError("Potential can be set to int only!")
        self.potential = value

    def get_potential(self):
        return self.potential

    def set_fill(self, value):
        if not isinstance(value, bool):
            raise ValueError("Fill can be set to int only!")
        self.fill = value

    def get_fill(self):
        return self.fill

    def set_scale(self, scale):
        self.scale = scale

    def get_proportions(self, scale=False):
        scale_factor = 1
        if scale is True:
            scale_factor = self.scale
        # print({key: (self.proportions[key] * scale_factor if self.proportions[key] is not None else self.proportions[key]) for key in self.proportions.keys()})
        temp = {key: (self.proportions[key] * scale_factor if self.proportions[key] is not None else self.proportions[key]) for key in self.proportions.keys()}
        return temp

    def add_proportions_dict(self, props : dict) -> None:
        for key in props.keys():
            self.add_proportions(key, props[key])

    def add_proportions(self, name, value, overwrite=True):
        if not overwrite and name in self.proportions.keys():
            print(f"Proportion {name} with value {value} was not set: it is already set to {self.proportions[name]}.")
            return
        self.proportions[name] = value

    def set_proportions(self, props: dict) -> None:
        for key in props.keys():
            self.add_proportions(key, props[key])

    def set_origin(self, origin):
        self.origin = self.to_xy(origin)
        self.add_proportions("origin", self.origin, overwrite=True)
        if self.get_max_x() is None:
            self.set_max_x(self.origin.x)
        if self.get_max_y() is None:
            self.set_max_y(self.origin.y)
        if self.get_min_x() is None:
            self.set_min_x(self.origin.x)
        if self.get_min_y() is None:
            self.set_min_y(self.origin.y)

    def get_origin(self, scale=False):
        if self.origin is None:
            return None
        if "origin" not in self.proportions.keys():
            self.add_proportions("origin", self.origin)
        test = self.get_proportions(scale=scale)
        temp = self.get_proportions(scale=scale)['origin']
        return temp

    def min_max_to_proportions(self, max_x, max_y, min_x, min_y):
        self.set_max_x(max_x)
        self.set_max_y(max_y)
        self.set_min_x(min_x)
        self.set_min_y(min_y)

    def set_max_x(self, max_x):
        self.max_x = max_x
        self.add_proportions("max_x", max_x)

    def set_max_y(self, max_y):
        self.max_y = max_y
        self.add_proportions("max_y", max_y)

    def set_min_x(self, min_x):
        self.min_x = min_x
        self.add_proportions("min_x", min_x)

    def set_min_y(self,min_y):
        self.min_y = min_y
        self.add_proportions("min_y", min_y)

    def update_max_min(self):
        self.check_correct_shape_settings(ingore_min_max = True)

    def check_correct_shape_settings(self, ingore_min_max=False):
        if None in [self.max_x, self.max_y, self.min_x, self.min_y] and not ingore_min_max:
            raise ValueError('Shape settings are incorrect: min/max is None.')
        if self.origin is None or not isinstance(self.origin.x, int) or not isinstance(self.origin.y, int):
            raise ValueError('Origin not set correctly: must contain two int [x,y].')

    def get_max_x(self, scale=False):
        return self.get("max_x", scale=scale)

    def get_max_y(self, scale=False):
        return self.get("max_y", scale=scale)

    def get_min_x(self, scale=False):
        return self.get("min_x", scale=scale)

    def get_min_y(self, scale=False):
        return self.get("min_y", scale=scale)

    def get_max(self):
        #todo convert to c.XY
        return self.get_max_x(), self.get_max_y()

    def get_min(self):
        # todo convert to c.XY
        return self.get_min_x(), self.get_min_y()

    def get(self, name, scale=False):
        if name not in self.proportions.keys():
            raise ValueError(f"Key {name} is not in proportions!")
        return self.get_proportions(scale=scale)[name]

    def get_gem_input(self, scale=True):
        self.check_correct_shape_settings()

    def to_xy(self, o):
        c = C.XY(0, 0)
        c.set_coordinates(o)
        return c

