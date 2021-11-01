from Simion.shapes import base
from Simion.shapes import circle
from Simion.shapes import box
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
        self.required_proportions = []
        self.min_max_to_proportions(origin.x, origin.y, origin.x, origin.y)

        self.complex_shape = True

    def define_required_proportions(self, props):
        # todo check correct shape of props
        self.required_proportions = props

    def check_correct_shape_settings(self, **kwargs):
        super(BasicCanvas, self).check_correct_shape_settings(**kwargs)
        for req_prop in self.required_proportions:
            if req_prop[0] not in self.proportions:
                raise ValueError(f"Value of \" {req_prop[0]} \" is not set!")
            if not isinstance(self.proportions[req_prop[0]], req_prop[1]):
                raise ValueError(
                    f"Value of \" {req_prop[0]} \" is not of the correct instance! Should be {req_prop[1]} instead of {type(self.proportions[req_prop[0]]).__name__}")

    def setup_canvas(self):
        logging.info("Setting up canvas.")
        # self.check_correct_canvas_settings()
        # todo pridat check spravneho nastaveni -- momentalne chyba, pokud nebyl spravne nastaven canvas, coz nebylo podstatne pro complex shapes

    def get_canvas_settings(self, name):
        if name not in self.canvas_settings.keys():
            logging.error(f"Setting \" {name} \" not found!")
            return
        else:
            return self.canvas_settings[name]

    def set_canvas_settings(self, name, value, overwrite=True):
        if name in self.canvas_settings.keys() and not overwrite:
            logging.warning(f"Setting \" {name} \" not set to new value, because overwrite is set to overwrite!")
        else:
            self.canvas_settings[name] = value.lower()

    def set_out_dir(self, out_dir):
        self.out_dir = pathlib.Path(out_dir)
        self.setup_dir()

    def setup_dir(self):
        self.out_dir.mkdir(parents=True, exist_ok=True)

    # def set_canvas_settings(self, dictionary):
    #     for key in dictionary.keys():
    #         if key not in self.canvas_settings.keys():
    #             continue
    #         self.canvas_settings[key] = dictionary[key].lower().strip()

    def get_current_pos(self):
        return self.current_pos

    def set_current_pos(self, pos):
        self.current_pos = self.to_xy(pos)

    # def set_origin(self, origin=c.XY(0, 0)):
    #     self.origin = c
    #     super(BasicCanvas, self).set_origin()

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
        max_x, max_y, min_x, min_y = new_max_min
        self.min_max_to_proportions(max_x, max_y, min_x, min_y)

    def check_correct_canvas_settings(self):
        if self.canvas_settings["symmetry"] not in ["cylindrical", "planar"]:
            raise ValueError("Symmetry must be set to either cylindrical or planar!")
        if self.canvas_settings["mirroring"] not in ['x', 'y', 'z']:
            raise ValueError("Mirroring must be set to either X,Y and Z")

    def save(self, scale=True):
        self.setup_dir()
        # todo check if file already exists and deal with it
        with open(self.out_dir.joinpath(pathlib.Path(self.name)), "w") as f:
            f.write(self.get_canvas_settings_text(scale=scale))
            f.write('\n\n')  # blank lines for better readability
            f.write(self.get_gem_input(scale=scale))

    def get_gem_input(self, scale=True):
        if len(self.shapes) == 0:
            return ""
        out = ""
        current_potential = None
        for shape in self.shapes:
            out += self.write_set_potential(shape, current_potential) if not shape.complex_shape else ''
            current_potential = shape.potential
            if current_potential is None:
                print(shape)
                print(current_potential)
            out += self.gem_from_shape(shape, scale=scale)
            out += '\n\t}\n}' if shape == self.shapes[-1] and not shape.complex_shape else '\n'
            # out += "\n"
        # out += '\t}\n}'
        return out

    def gem_from_shape(self, shape, scale=True):
        out = ("\t\twithin{" if shape.fill else "notin{") if not shape.complex_shape else ''
        out += shape.get_gem_input(scale=scale)
        out += "}" if not shape.complex_shape else ''
        return out

    def write_set_potential(self, shape, current_potential):
        if shape.potential is None:
            return ''
        end = "\t}\n}\n" if current_potential is not None else ''
        if shape.potential == current_potential:
            return ""
        else:
            return end + f"e({shape.potential})" + "{fill{\n"

    def get_canvas_settings_text(self, scale=True):
        self.check_correct_canvas_settings()
        s = self.scale if scale else 1
        return f"PA_define({(self.get_max_x() - self.origin.x) * s}, {(self.get_max_y() - self.origin.y) * s}, 1, {self.canvas_settings['symmetry']}, {self.canvas_settings['mirroring'].lower()})"

    def add_shape(self, shape, potential=1, fill=True):
        # if shape is a complex shape/other canvas, it needs to be setup
        if hasattr(shape, "setup_canvas") and callable(getattr(shape, "setup_canvas")):
            shape.setup_canvas()
        shape.set_scale(self.scale)
        shape.set_potential(potential)
        shape.fill = fill
        self.shapes += [shape]
        self.update_max_min()

    def get_last_shape(self):
        return self.shapes[-1]

    def add_circle(self, r, move_current_pos=True, **kwargs):
        cir = circle.Circle(self.get_current_pos(), r)
        if move_current_pos:
            self.set_current_pos(c.XY(cir.get_max_x(scale=False), cir.get_origin().y))
        self.add_shape(cir, **kwargs)
        return cir

    def add_rectangle(self, length, height, move_current_pos=True, **kwargs):
        b = box.Box(length, height, left_down_corner=self.get_current_pos())
        if move_current_pos:
            self.set_current_pos(c.XY(b.get_max_x(scale=False), b.get_origin().y))
        self.add_shape(b, **kwargs)
        print('Box max y: ' + str(b.get_max_y()))
        return b

    def add_space(self, length, height):
        self.current_pos += c.XY(length, height)

        max_x = self.max_x if self.max_x > self.current_pos.x else self.current_pos.x
        max_y = self.max_y if self.max_y > self.current_pos.y else self.current_pos.y
        min_x = self.min_x if self.min_x < self.current_pos.x else self.current_pos.x
        min_y = self.min_y if self.min_y < self.current_pos.y else self.current_pos.y
        self.min_max_to_proportions(max_x, max_y, min_x, min_y)

    def add_vertical_space(self, length):
        self.add_space(length, 0)

    def add_horizontal_space(self, height):
        self.add_space(0, height)

    # def add_space_before(self, s):
    #     self.set_min_x(self.get_min_x() - s)
    #
    # def add_space_after(self, s):
    #     self.set_max_x(self.get_max_x() + s)
    #
    def add_space_above(self, s):
        print(self.get_max_y())
        self.set_max_y(self.get_max_y() + s)
        print(self.get_max_y())
    #
    # def add_space_bellow(self, s):
    #     self.set_min_y(self.get_min_y() - s)

    def set_scale(self, scale):
        super(BasicCanvas, self).set_scale(scale)
        for shape in self.shapes:
            shape.set_scale(scale)