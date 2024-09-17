"""
ZPL functions to translate pillow commands to ZPL commands
and dpi, pixels all to their mm counterparts

dpmm can be interpreted as ppmm
all sizing info can be interpreted as ((width, height), dpmm, "mm")

for img:
write_graphic takes in mm,

for zpl code:
origin coordinates on the label are defined in mm
barcode, text, sizes are defined in dots (aka pixels), take dpmm * pix


Printer interface:
"""

import zpl
from zebra import Zebra
from PIL import Image


def zpl_size_translator(
    info: tuple[tuple[int, int], int, str],
    secondary_info=None,
) -> tuple[tuple[float, float], int]:
    """
    Gives everything back in mm terms
    """
    size = info[0]
    unit = info[1]
    type = info[2]
    match type:
        case "inches":
            size_mm = tuple(s * 25.4 for s in size)
            dpmm = round(unit / 25.4)
        case "pixels":
            pixel_to_mm = 25.4 / unit
            size_mm = tuple(s * pixel_to_mm for s in size)
        case "mm":  # given secondary info to translate
            assert secondary_info is not None, "No secondary info provided to translate"
            size = secondary_info
            size_mm = tuple(s / unit for s in size)
            dpmm = unit
    return (size_mm, dpmm, "mm")


def img_to_print(
    temp_label_paths: list[str],
    label_settings_mm: tuple[tuple[int, int], int],
) -> object:
    """
    generator to draw img graphics into zpl code (literally)
    """
    print(label_settings_mm)
    """
    ROTATE 90 FOR CEVA DEMO
    """
    label_settings_print = (
        (label_settings_mm[0][1], label_settings_mm[0][0]),
        label_settings_mm[1],
        label_settings_mm[2],
    )
    for i, label_path in enumerate(temp_label_paths):
        zpl_label = zpl.Label(
            width=label_settings_print[0][0],
            height=label_settings_print[0][1],
            dpmm=label_settings_mm[1],
        )
        zpl_label.origin(0, 0)
        __temp_label_img = Image.open(label_path)
        __rotated_img = __temp_label_img.rotate(90, expand=True)
        zpl_label.write_graphic(
            __rotated_img,
            width=label_settings_print[0][0],
            height=label_settings_print[0][1],
            compression_type="A",
        )
        zpl_label.endorigin()
        # pure_label_path = PurePath(label_path).stem + ".zpl"
        yield zpl_label


def img_to_zpl(
    temp_label_paths: list[str],
    label_settings_mm: tuple[tuple[int, int], int],
) -> object:
    """
    generator to draw img graphics into zpl code (literally)
    """
    print(label_settings_mm)
    for i, label_path in enumerate(temp_label_paths):
        zpl_label = zpl.Label(
            width=label_settings_mm[0][0],
            height=label_settings_mm[0][1],
            dpmm=label_settings_mm[1],
        )
        zpl_label.origin(0, 0)
        __temp_label_img = Image.open(label_path)
        zpl_label.write_graphic(
            __temp_label_img,
            width=label_settings_mm[0][0],
            height=label_settings_mm[0][1],
            compression_type="A",
        )
        zpl_label.endorigin()
        # pure_label_path = PurePath(label_path).stem + ".zpl"
        yield zpl_label


def write_zpl(
    img_coords_maps: list[dict[int, tuple[object, tuple[int, int], tuple[int, int]]]],
    element_maps: list[dict[int, dict[str, object, int]]],
    margins_mm: tuple[int, int],
    zpl_translator_fn: object,
    label_settings_mm,
    label_map,
) -> object:
    """
    generator to write zpl code from provided coordinates,
    element types (barcode type, qrcode ver, etc.) amd margins
    """
    print(label_settings_mm)
    for i, ele_map in enumerate(element_maps):
        zpl_label = zpl.Label(
            width=label_settings_mm[0][0],
            height=label_settings_mm[0][1],
            dpmm=label_settings_mm[1],
        )
        pos_fns_pair = zpl_translator_fn(ele_map, img_coords_maps[i])
        pos_fns_pair = dict(pos_fns_pair)
        x, y = margins_mm[0][0] / 2, margins_mm[0][1]
        print("ele_map", ele_map)
        print("pos_fns_pair", pos_fns_pair)
        for pos, fn in pos_fns_pair.items():
            if label_map[pos] == "bar":
                x -= margins_mm[0][0] / 2
                y += margins_mm[0][1] / 2
            zpl_label.origin(x, y)
            fn(zpl_label)
            zpl_label.endorigin()
            if label_map[pos] == "bar":
                x -= margins_mm[0][0] / 2
                y -= margins_mm[0][1] / 2
            height_mm = zpl_size_translator(
                label_settings_mm, img_coords_maps[i][pos][2]
            )
            y += height_mm[0][1] + (
                margins_mm[0][1]
            )  # dict index -> pos -> size -> height

        yield zpl_label


def create_zpl_fn_translator(element_fn_map, label_settings_mm, margins_mm):
    bar_types = {
        "GS1-128": "C",
    }
    """
    For margins, we need to make a virtual label that is smaller than the original,
    create all the elements there, then append to the real label with the margins
    """
    real_size = label_settings_mm[0]
    virtual_size = (
        (real_size[0] - (2 * margins_mm[0][0])),
        (real_size[1] - (2 * margins_mm[0][1])),
    )
    virtual_label_settings_mm = (
        virtual_size,
        label_settings_mm[1],
        label_settings_mm[2],
    )
    print(virtual_label_settings_mm)

    def zpl_fn_translator(element_map, img_coord_map):
        """
        segno and barcode libraries provide us with optimised parameters,
        we want to use them to create similar fns to look as close as possible
        to the preview scene

        takes the element_fn_map, relevant parameters like barcode type,
        font size, qr ver etc, and provides the fn and kwargs for write_zpl

        list of zpl barcode types: https://gist.github.com/metafloor/773bc61480d1d05a976184d45099ef56
        we are hardcoding Code_128, C type (for now) TODO: give user choice

        list of zpl text types: https://minisoft.com/support/index.php/zebra-font-support/
        check the width of the font_mask, and choose the appropriate line_width

        Unfortunately, it seems that ZPL does not support custom QR code sizes, will use img for now

        TODO: THIS IS QUITE BROKEN, WILL WORK ON IT
        """
        for pos, (fn, _) in element_fn_map.items():
            match fn.__name__:
                case "gen_qr":
                    # mask = element_map[pos]["mask"]
                    # ecl = element_map[pos]["ECL"]
                    # qr_size_pix = img_coord_map[pos][2]
                    # qr_size_mm = zpl_size_translator(label_settings_mm, qr_size_pix)
                    # yield pos, lambda label_obj: label_obj.barcode(
                    #     code=element_map[pos]["label_text"],
                    #     mask=mask,
                    #     errorCorrection=ecl,
                    #     barcode_type="Q",
                    #     magnification=3,
                    # )
                    qr_img = img_coord_map[pos][0]
                    qr_size_mm = zpl_size_translator(
                        virtual_label_settings_mm, qr_img.size
                    )
                    yield pos, lambda label_obj, qr_img=qr_img, width=virtual_label_settings_mm[
                        0
                    ][
                        0
                    ] + margins_mm[
                        0
                    ][
                        0
                    ], height=virtual_label_settings_mm[
                        0
                    ][
                        0
                    ] + margins_mm[
                        0
                    ][
                        1
                    ]: label_obj.write_graphic(
                        qr_img,
                        width=width,
                        height=height,
                        compression_type="A",
                    )
                case "gen_barcode":
                    bar_type = element_map[pos]["barcode_type"]
                    bar_size_pix = img_coord_map[pos][2]
                    bar_size_mm = zpl_size_translator(
                        virtual_label_settings_mm, bar_size_pix
                    )
                    zpl_bar_type = bar_types[bar_type]
                    yield pos, lambda label_obj, code=element_map[pos][
                        "label_text"
                    ], height=int(
                        bar_size_mm[0][1] * virtual_label_settings_mm[1]
                    ), barcode_type=zpl_bar_type: label_obj.barcode(
                        code=code,
                        height=height,
                        barcode_type=barcode_type,
                        print_interpretation_line="N",
                    )

                case "gen_font":
                    text_size_pix = img_coord_map[pos][2]  # gets the pixel size
                    text_size_mm = zpl_size_translator(
                        virtual_label_settings_mm, text_size_pix
                    )
                    text_width = text_size_mm[0][0]
                    text_height = text_size_mm[0][1]
                    yield pos, lambda label_obj, text=element_map[pos][
                        "label_text"
                    ], char_width=(
                        text_width / len(element_map[pos]["label_text"])
                    ), char_height=text_height: label_obj.write_text(
                        text=text,
                        char_width=char_width,
                        char_height=char_height + 1,
                        justification="J",
                        font="E",
                    )

    return zpl_fn_translator


def save_zpl(zpl_label: object, zpl_save_path: str) -> None:
    print(zpl_save_path)
    zpl_text = zpl_label.dumpZPL()
    with open(zpl_save_path, "x") as zpl_file:
        zpl_file.write(zpl_text)


def preview_zpl(zpl_label):
    zpl_label.preview()


def interface_printer(
    label_settings: tuple[tuple[int], int, str],
):
    """Finds and interface with ZPL printers"""
    """ROTATED 90 FOR CEVA DEMO"""
    label_width = label_settings[0][1] * label_settings[1]
    label_height = (label_settings[0][0] * label_settings[1], 0)
    print(label_height, label_width)
    z = Zebra()
    printer_queues = z.getqueues()
    print(printer_queues)
    for printer in printer_queues:
        if "Zebra" in printer:
            z.setqueue(printer)
    z.setup()
    return z
