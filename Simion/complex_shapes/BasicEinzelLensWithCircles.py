from Simion.canvas import basic_canvas
from Simion.complex_shapes import BasicEinzelCylinder
from Simion.common import coordinate2D as c


class BasicEinzelLensWithCircle(basic_canvas.BasicCanvas):
    def __init__(self, **kwargs):
        super(BasicEinzelLensWithCircle, self).__init__(**kwargs)
        self.define_required_proportions([
            ['einzel_length', int],
            ['einzel_height', int],
            ['circle_radius', int],
            ['einzel_radius', int],
            ['space', int]
        ])

    def add_einzel_cylinder(self, move_current_pos=True, **kwargs):
        cyl = BasicEinzelCylinder.EinzelCylinderWithCircle(origin=self.get_current_pos())
        cyl.set_proportions({'einzel_length': self.get('einzel_length'), 'einzel_height': self.get('einzel_height'),
                             'circle_radius': self.get('circle_radius')})
        self.add_shape(cyl, **kwargs)
        if move_current_pos:
            self.set_current_pos(c.XY(cyl.get_max_x(scale=False), cyl.get_origin().y))

    def setup_canvas(self):
        super(BasicEinzelLensWithCircle, self).setup_canvas()
        self.add_horizontal_space(self.get('einzel_radius'))
        self.add_einzel_cylinder(potential=0)
        self.add_space(self.get('space'), 0)
        self.add_einzel_cylinder(potential=1)
        self.add_space(self.get('space'), 0)
        self.add_einzel_cylinder(potential=2)
