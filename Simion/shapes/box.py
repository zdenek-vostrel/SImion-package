from Simion.shapes import base
from Simion.common import coordinate2D as C


class Box(base.Base):
    def __init__(self, length, height, center=None, left_down_corner=None, left_up_corner=None, right_up_corner=None,
                 right_down_corner=None):
        super(Box, self).__init__(proportions={'length': length, 'height':height})
        self.length = abs(length)
        self.height = abs(height)
        self.left_down_corner = None

        if center is not None:
            self.set_from_center(center)
        elif left_down_corner is not None:
            self.set_from_left_down_corner(left_down_corner)
        elif left_up_corner is not None:
            self.set_from_left_up_corner(left_up_corner)
        elif right_down_corner is not None:
            self.set_from_left_down_corner(right_down_corner)
        elif right_up_corner is not None:
            self.set_from_left_up_corner(right_up_corner)
        else:
            raise KeyError("One of the origin options must be chosen!")

        self.add_proportions_dict({"length": length, "height": height, "left_down_corner": self.left_down_corner})

        self.update_max_min()

    def set_common(self, c):
        c = self.to_xy(c)
        if self.origin is None:
            self.set_origin(c)
        return c

    def set_from_center(self, center):
        c = self.set_common(center)
        self.set_from_left_down_corner(c - [int(self.length/2), int(self.height/2)])

    def set_from_left_down_corner(self, left_down_corner):
        left_down_corner = self.set_common(left_down_corner)
        self.left_down_corner = left_down_corner

    def set_from_left_up_corner(self, left_up_corner):
        c = self.set_common(left_up_corner)
        self.set_from_left_down_corner(c - [0, self.height])

    def set_from_right_up_corner(self, right_up_corner):
        c = self.set_common(right_up_corner)
        self.set_from_left_down_corner(c - [self.length, self.height])

    def set_from_right_down_corner(self, right_down_corner):
        c = self.set_common(right_down_corner)
        self.set_from_left_down_corner(c - [self.length, 0])

    def get_left_down_corner(self, scale=False):
        return self.get_proportions(scale=scale)['left_down_corner']

    def get_left_up_corner(self, scale=False):
        return self.get_left_down_corner(scale=scale) + [0, self.get_height(scale=scale)]

    def get_right_down_corner(self, scale=False):
        return self.get_left_down_corner(scale=scale) + [self.get_length(scale=scale), 0]

    def get_right_up_corner(self, scale=False):
        return self.get_left_down_corner(scale=scale) + [self.get_length(scale=scale), self.get_height(scale=scale)]

    def get_length(self, scale=False):
        return self.get_proportions(scale=scale)['length']

    def get_height(self, scale=False):
        return self.get_proportions(scale=scale)['height']

    def update_max_min(self):
        min_x = self.get_left_down_corner().x
        min_y = self.get_left_down_corner().y
        max_x = self.get_right_up_corner().x
        max_y = self.get_right_up_corner().y
        self.min_max_to_proportions(max_x, max_y, min_x, min_y)
        super(Box, self).update_max_min()

    def get_gem_input(self, scale=True):
        super(Box, self).get_gem_input()
        ldc = self.get_left_down_corner(scale=scale)
        print(self.get_right_up_corner())
        length = self.get_length(scale=scale)
        height = self.get_height(scale=scale)
        return f"box({ldc.x},{ldc.y},{ldc.x+length},{ldc.y+height})"

