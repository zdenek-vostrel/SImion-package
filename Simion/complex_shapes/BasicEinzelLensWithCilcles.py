from Simion.canvas import basic_canvas
from Simion.complex_shapes import BasicEinzelCylinder
from Simion.common import coordinate2D as c


class BasicEinzelLensWithCircle(basic_canvas.BasicCanvas):
    def __init__(self, einzel_length, einzel_height, circle_radius, space, **kwargs):
        self.einzel_length = abs(einzel_length)
        self.einzel_height = abs(einzel_height)
        self.circle_radius = abs(circle_radius)
        self.space = abs(space)
        super(BasicEinzelLensWithCircle, self).__init__(**kwargs)

    def add_einzel_cylinder(self, move_current_pos=True, **kwargs):
        cyl = BasicEinzelCylinder.EinzelCylinderWithCircle(self.einzel_length, self.einzel_height, self.circle_radius, origin=self.get_current_pos())
        if move_current_pos:
            self.set_current_pos(c.XY(cyl.get_max_x(scale=False), cyl.get_origin().y))
        self.add_shape(cyl, **kwargs)

    def setup_canvas(self):
        super(BasicEinzelLensWithCircle, self).setup_canvas()
        self.add_einzel_cylinder(potential=0)
        self.add_space(self.space, 0)
        self.add_einzel_cylinder(potential=1)
        self.add_space(self.space, 0)
        self.add_einzel_cylinder(potential=2)
