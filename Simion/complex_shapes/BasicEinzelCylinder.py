from Simion.canvas import basic_canvas


class EinzelCylinderWithCircle(basic_canvas.BasicCanvas):
    def __init__(self, **kwargs):
        self.define_required_proportions([
            ['einzel_length', int],
            ['einzel_height', int],
            ['circle_radius', int]
        ])
        super(EinzelCylinderWithCircle, self).__init__(**kwargs)

    def set_potential(self, value):
        super(EinzelCylinderWithCircle, self).set_potential(value)
        for shape in self.shapes:
            shape.set_potential(value)

    def setup_canvas(self):
        super(EinzelCylinderWithCircle, self).setup_canvas()
        self.add_space(self.get('circle_radius'), 0)
        self.add_rectangle(self.get('einzel_length'), self.get('einzel_height'), move_current_pos=False)
        self.add_space(0, int(self.get('einzel_height') / 2))
        self.add_circle(self.get('circle_radius'), move_current_pos=False)
        self.add_space(self.get('einzel_length'), 0)  # does not create a space but only updates the current position
        self.add_circle(self.get('circle_radius'))
