from Simion.canvas import basic_canvas
from Simion.complex_shapes import BasicEinzelLensWithCilcles as einzel
from Simion.common import coordinate2D as c

class EinzelLensBasic(basic_canvas.BasicCanvas):
    def __init__(self, **kwargs):
        super(EinzelLensBasic, self).__init__(**kwargs)
        self.define_required_proportions([
            ['einzel_length', int],
            ['einzel_height', int],
            ['circle_radius', int],
            ['space_between', int],
            ['space_before', int],
            ['space_after', int],
            ['space_above', int]
        ])

    def add_einzel(self, move_current_pos=True, **kwargs):
        ein = einzel.BasicEinzelLensWithCircle(origin=self.get_current_pos())
        ein.set_proportions({'einzel_length': self.get('einzel_length'), 'einzel_height': self.get('einzel_height'),
                             'circle_radius': self.get('circle_radius'), 'space': self.get('space_between')})
        if move_current_pos:
            print(ein.get_max_x(scale=False))
            self.set_current_pos(c.XY(ein.get_max_x(scale=False), ein.get_origin().y))
        self.add_shape(ein, **kwargs)

    def setup_canvas(self):
        super(EinzelLensBasic, self).setup_canvas()
        self.add_space(self.get("space_before"), 0)
        self.add_einzel()
        self.add_space(self.get("space_after"), 0)
        self.add_space_above(self.get('space_above'))
