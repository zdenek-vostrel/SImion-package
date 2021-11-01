from Simion.canvas import basic_einzel_lens_canvas


def main():
    canvas = basic_einzel_lens_canvas.EinzelLensBasic()
    canvas.set_canvas_settings('symmetry', 'cylindrical')
    canvas.set_canvas_settings('mirroring', 'y')
    canvas.set_proportions({
        'einzel_length': 30,
        'einzel_height': 10,
        'circle_radius': 5,
        'einzel_radius': 10,
        'space_between': 10,
        'space_before': 20,
        'space_after': 20,
        'space_above': 10
    })
    canvas.setup_canvas()
    canvas.save()



if __name__ == '__main__':
    main()
