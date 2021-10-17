from Simion.shapes import box

class Space(box.Box):
    def __init__(self, length, height, **kwargs):
        self.sgn_length = 1 if length >= 0 else -1
        self.sgn_height = 1 if length >= 0 else -1
        super(Space, self).__init__(length, height, **kwargs)

    def get_gem_input(self):
        self.check_correct_shape_settings()
        return