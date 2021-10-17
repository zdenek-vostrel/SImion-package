from Simion.shapes import base
from Simion.shapes import circle
from Simion.shapes import box
from Simion.shapes import space
from Simion.common import coordinate2D as c
import logging
import pathlib


class BasicCanvas(base.Base):
    def __init__(self, origin=c.XY(0, 0), name="shape", scale=1, out_dir="GEMS", **kwargs):
        super(BasicCanvas, self).__init__(**kwargs)
        self.set_origin(origin)
        self.current_pos = self.get_origin(scale=False)
        self.shapes = []
        self.canvas_settings = {
            "type": None,
            "symmetry": None,
            "mirroring": None
        }
        self.scale = scale
        self.name = name
        self.out_dir = pathlib.Path(out_dir)
        self.setup_dir()

    def set_out_dir(self, out_dir):
        self.out_dir = pathlib.Path(out_dir)
        self.setup_dir()

    def setup_dir(self):
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def set_canvas_settings(self, dictionary):
        for key in dictionary.keys():
            if key not in self.canvas_settings.keys():
                continue
            self.canvas_settings[key] = dictionary[key].lower().strip()

    def get_current_pos(self):
        return self.current_pos

    def set_current_pos(self, pos):
        self.current_pos = self.to_xy(pos)

    def set_origin(self, origin=c.XY(0, 0)):
        self.origin = c
        super(BasicCanvas, self).set_origin()

    def update_max_min(self):
        super(BasicCanvas, self).update_max_min()
        new_max_min = []
        for m in ["max_x", "max_y", "min_x", "min_y"]:
            adjust = -1 if m[:3] == "min" else 1
            if self.get(m, scale=False) is None:
                new_max_min += [self.get(m, scale=False)]
                continue
            if self.get_last_shape().get(m, scale=False) * adjust > self.get(m, scale=False) * adjust:
                new_max_min += [self.get_last_shape().get(m, scale=False)]
            else:
                new_max_min += [self.get(m, scale=False)]

    def check_correct_canvas_settings(self):
        if self.canvas_settings["symmetry"] not in ["cylyndrical", "planar"]:
            raise ValueError("Symmetry must be set to either cylyndrical or planar!")
        if self.canvas_settings["mirroring"] not in ['x', 'y', 'z']:
            raise ValueError("Mirroring must be set to either X,Y and Z")

    def save(self, scale=True):
        #todo check if file already exists and deal with it
        with open(self.out_dir.joinpath(pathlib.Path(self.name)), "w") as f:
            f.write(self.get_canvas_settings(scale=scale))
            f.write(self.get_gem_input(scale=scale))

    def get_gem_input(self, scale=True):
        if len(self.shapes) == 0:
            return ""
        out = ""
        current_potential = None
        for shape in self.shapes:
            out += self.set_potential(shape, current_potential)
            current_potential = shape.potential
            out += self.gem_from_shape(shape, scale=scale)
            out += "\n"
        out += "\t}"
        return out

    def gem_from_shape(self, shape, scale=True):
        out = "\t\twithin{" if shape.fill else "notin{"
        out += shape.get_gem_input(scale=scale)
        out += "}"
        return out

    def set_potential(self, shape, current_potential):
        end = "\t}}\n" if current_potential is not None else ""
        if shape.potential == current_potential:
            return ""
        else:
            return end+f"\te({shape.potential})"+"{fill{\n"

    def get_canvas_settings(self, scale=True):
        self.check_correct_canvas_settings()
        s = self.scale if scale else 1
        return f"PA_define({(self.current_pos.x - self.origin.x) * s}, {(self.current_pos.y - self.origin.y) * s}, 1, {self.canvas_settings['symmetry']}, {self.canvas_settings['mirroring'].upper()})"

    def add_shape(self, shape, potential=1, fill=True):
        shape.set_scale(self.scale)
        shape.potential = potential
        shape.fill = fill
        self.shapes += [shape]
        self.update_max_min()

    def get_last_shape(self):
        return self.shapes[-1]

    def add_circle(self, r, **kwargs):
        cir = circle.Circle(self.get_current_pos(), r)
        self.set_current_pos(c.XY(cir.get_max_x(scale=False), cir.get_origin().y))
        self.add_shape(cir, **kwargs)

    def add_rectangle(self, length, height, **kwargs):
        b = box.Box(length, height, left_down_corner=self.get_current_pos())
        self.set_current_pos(c.XY(b.get_max_x(scale=False), b.get_origin().y))
        self.add_shape(b, **kwargs)

    def add_space(self, length, height):
        self.current_pos += c.XY(length, height)

    def add_vertical_space(self, length):
        self.add_space(length, 0)

    def add_horizontal_space(self, height):
        self.add_space(0, height)
