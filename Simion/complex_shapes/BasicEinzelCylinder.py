from Simion.canvas import basic_canvas


class EinzelCylinderWithCircle(basic_canvas.BasicCanvas):
    def __init__(self, einzel_length, einzel_height, circle_radius, **kwargs):
        self.einzel_length = abs(einzel_length)
        self.einzel_height = abs(einzel_height)
        self.circle_radius = abs(circle_radius)
        super(EinzelCylinderWithCircle, self).__init__(**kwargs)

    def set_potential(self, value):
        super(EinzelCylinderWithCircle, self).set_potential()
        for shape in self.shapes:
            shape.set_potential(value)

    def setup_canvas(self):
        super(EinzelCylinderWithCircle, self).setup_canvas()
        self.add_space(self.circle_radius, 0)
        self.add_rectangle(self.einzel_length, self.einzel_height, move_current_pos=False)
        self.add_space(0, int(self.einzel_height / 2))
        self.add_circle(self.circle_radius, move_current_pos=False)
        self.add_space(self.einzel_length, 0)  # does not create a space but only updates the current position
        self.add_circle(self.circle_radius)
