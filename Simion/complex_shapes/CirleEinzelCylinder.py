from Simion.canvas import basic_canvas


class EinzelCylinderCircle(basic_canvas.BasicCanvas):
    def __init__(self, **kwargs):
        self.define_required_proportions([
            ['einzel_height', int],
            ['circle_vertical_alignment', int]
        ])
        super(EinzelCylinderCircle, self).__init__(**kwargs)

    def set_potential(self, value):
        super(EinzelCylinderCircle, self).set_potential(value)
        for shape in self.shapes:
            shape.set_potential(value)

    def setup_canvas(self):
        super(EinzelCylinderCircle, self).setup_canvas()
        radius = self.get("einzel_height") + self.get("circle_vertical_alignment")
        self.add_space(radius, radius)
        self.add_circle(radius, move_current_pos=False)
