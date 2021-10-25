from Simion.shapes import base
from Simion.common import coordinate2D as C


class Circle(base.Base):
    def __init__(self, center, r, scale=1):
        self.scale = scale
        self.set_center(center)
        self.set_origin(center)
        super(Circle, self).__init__(proportions={'r': r})
        self.r = self.get_proportions(scale=False)['r']
        self.center = self.get_proportions(scale=False)['center']

    def update_max_min(self):
        r = self.get_proportions(scale=False)['r']
        center = self.get_proportions(scale=False)['center']
        max_x = center.x + r
        max_y = center.y + r
        min_x = center.x - r
        min_y = center.y - r
        self.min_max_to_proportions(max_x, max_y, min_x, min_y)
        super(Circle, self).update_max_min()

    def get_gem_input(self, scale=True):
        super(Circle, self).get_gem_input()
        center = self.get_proportions(scale=scaled)['center']
        r = self.get_proportions(scale=scaled)['r']
        return f"circle({center.x},{center.y},{r})"

    def check_correct_shape_settings(self, **kwargs):
        super(Circle, self).check_correct_shape_settings(**kwargs)
        for var in [self.r, self.center.x, self.center.y]:
            if not isinstance(var, float) and not isinstance(var, int):
                raise ValueError(
                    'Center must contain two values: [x,y], both of them must be int/float, r must be r/float.')

    def set_center(self, center):
        center = self.to_xy(center)
        self.add_proportions("center", center)

    def get_center(self, scale=False):
        return self.get_proportions(scale=scale)['center']

    def get_r(self, scale=True):
        return self.get_proportions(scale=scale)['r']
