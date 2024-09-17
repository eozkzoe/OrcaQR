"""
Tools used in generating labels

DEFINITIONS:
 - img_coords_map {pos: (img_asset, tuple(current_coord), size)}

"""

import segno
from barcode import Gs1_128
from barcode.writer import ImageWriter
import tempfile
from PIL import Image, ImageFont, ImageDraw
from . import exttools
import code
from pprint import pprint
import math


def label_size_translator(
    info: tuple[tuple[int, int], int, str],
    to_unit: str,
    secondary_info=None,
) -> tuple[tuple[float, float], int]:
    """
    Gives everything back in mm terms
    """
    size = info[0]
    unit = info[1]
    type = info[2]
    to_unit_dict = {"inch_mm": 25.4}
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


def gen_asset_maps(
    element_maps,
    element_fn_map,
    element_regions_map,
    label_map,
    regions,
    element_resizeable,
    margins,
    alignment,
    progress_dialog,
):
    """
    Now the element map should contain a dict

    element_fn_map: (index, gen_fn, unpack_fn)

    element_maps: list of dicts, one label per dict

    landscape or portrait is actually just decided by the regions,
    an qt bbox that determines which area elements are assigned to

    QR is always element 0
    """
    _temp_coords_array = []
    desc_maps = []
    step = 0
    for element_map in element_maps:
        img_coords_map, desc_map = arrange_label(
            element_map,
            element_fn_map,
            element_regions_map,
            label_map,
            regions,
            element_resizeable,
            margins,
            alignment,
        )

        _temp_coords_array.append(img_coords_map)
        desc_maps.append(desc_map)
        step += 1
        progress_dialog.setValue(step)
        progress_dialog.setLabelText(
            f"Loading {step}/{progress_dialog.maximum()} labels"
        )

    return _temp_coords_array, desc_maps


def text_mapping(
    text_encoding_map: dict[str, str],
    label_map: dict[int, str],
    selected_rows_info: list[list[tuple[str, str]]],
) -> dict[str, str]:
    """
    text_encoding_map: dictionary of [header, positions] which indicates the
    positions where text should be encoded/placed

    selected_rows_info: list of list of tuples (selected_label, header), which allows
    us to pair the label to the encoding type

    It applies selected labels to encoded positions, concatenates with a comma if multiple
    labels are mapped to a single position,
    and returns a list of list of dicts with its respective positions:strings

    return example: {0: 'text1,text2', 1: 'text1', 2: 'text1', 3: 'text2'}
    """
    position_text_pair_rows = []
    title_posits = [i for i, t in label_map.items() if t == "title"]

    def get_pos_text_in_map(row):
        for data, header in row:
            if header in text_encoding_map:
                non_titles = list(set(text_encoding_map[header]) - set(title_posits))
                non_titles.sort()

                titles = list(set(text_encoding_map[header]) - set(non_titles))
                titles.sort()
                yield tuple(non_titles), data
                yield tuple(titles), header

    for row in selected_rows_info:
        row_data = {}
        for pos, text in get_pos_text_in_map(row):
            if tuple(pos) not in row_data:
                row_data[pos] = text
            else:
                row_data[pos] += f",{text}"

        position_text_pair_rows.append(row_data)
    return position_text_pair_rows


def element_mapper_factory(label_map: dict[int, str]):
    """
    To include multiple fields dynamically

    Returns a {index: (gen_fn, unpack_fn)}
    """
    sorted_label_map = dict(sorted(label_map.items()))
    for pos, ele_type in sorted_label_map.items():
        match ele_type:
            case "qr":
                yield pos, (gen_qr, unpack_qr_map)
            case "bar":
                yield pos, (gen_barcode, unpack_bar_map)
            case "text":
                yield pos, (gen_font, unpack_text_map)
            case "title":
                yield pos, (gen_title, unpack_title_map)
            case _:
                raise Exception("Received unexpected element")


def create_element_maps(
    element_region_map,
    regions,
    element_fn_map,
    position_text_pair_rows,
    font_name,
    title_font_name,
) -> list[dict]:
    """
    returns a list of dictionaries that contains the assets at every position

    filters the arguments required for each function
    """
    module_size = None
    element_maps = []
    for single_position_text_pair_row in position_text_pair_rows:
        element_map = {}
        for pos, (fn, _) in element_fn_map.items():
            label_string = ""
            for posits, text in single_position_text_pair_row.items():
                if pos in posits:
                    label_string += f"{text},"
            label_string = label_string[:-1]
            match fn.__name__:
                case "gen_qr":
                    element_map[pos] = fn(
                        label_string, regions[element_region_map[pos]]["size"]
                    )
                    module_size = element_map[pos]["module_size"]
                case "gen_barcode":
                    element_map[pos] = fn(label_string)
                case "gen_font":
                    element_map[pos] = fn(
                        label_string,
                        regions[element_region_map[pos]]["size"],
                        font_name,
                    )
                case "gen_title":
                    element_map[pos] = fn(
                        label_string,
                        regions[element_region_map[pos]]["size"],
                        title_font_name,
                    )
        element_maps.append(element_map)
    return element_maps, module_size


def gen_qr(label_string: str, region_size: tuple[int, int]) -> str:
    qr, module_size = auto_qr_sizing(label_string=label_string, region_size=region_size)
    return {
        "asset": qr,
        "label_text": label_string,
        "module_size": module_size,
        "QR_version": qr.version,
        "mask": qr.mask,
        "ECL": qr.error,
    }


def gen_barcode(label_string: str) -> str:
    barcode = Gs1_128(label_string, writer=ImageWriter())
    barcode.text = ""
    return {
        "asset": barcode,
        "label_text": label_string,
        "module_width": barcode.default_writer_options["module_width"],
        "barcode_type": barcode.name,
    }


def gen_title(
    label_string: str,
    region_size: tuple[int, int],
    font_name: str,
):
    # wrapper to differentiate title fonts
    return gen_font(label_string, region_size, font_name)


def gen_font(
    label_string: str,
    region_size: tuple[int, int],
    font_name: str,
) -> object:
    font_path = exttools.get_font_path(font_name=font_name)
    font, font_size = auto_font(font_path, label_string, region_size)
    return {
        "asset": font,
        "label_text": label_string,
        "font": font_name,
        "font_size": font_size,
    }


def get_label_size(label_settings: tuple[tuple[int, int], int, str]):
    dims = label_settings[0]
    ppi = label_settings[1]
    type = label_settings[2]
    if type == "inches":
        _label_size_x = dims[0] * ppi
        _label_size_y = dims[1] * ppi
    return _label_size_x, _label_size_y


def get_label_regions(
    label_settings: tuple[tuple[int, int], int, str], element_regions
):
    ppi = label_settings[1]
    type = label_settings[2]
    # multiply everything by ppi
    if type == "inches":
        _element_regions = {
            i: {k: [int(x * ppi) for x in v] for k, v in region_dict.items()}
            for i, region_dict in element_regions.items()
        }
    return _element_regions


def unpack_qr_map(qr_info, label_width):
    """
    unpack the qr tuple
    qr_info: (segno qr object, module, desc)
    """
    qr = qr_info["asset"]
    with tempfile.NamedTemporaryFile(
        prefix=f"qr", suffix=".png", delete=False
    ) as temp_qr:
        qr.save(
            temp_qr, scale=qr_info["module_size"], border=0
        )  # scale beyond label size for resize quality
        __temp_qr_img = Image.open(temp_qr)
        __temp_qr_img = __temp_qr_img.resize(
            (
                label_width,
                label_width,
            )  # basically just the width of the label
        )
        size = __temp_qr_img.size
        desc = desc_builder(qr_info)
        return __temp_qr_img, size, desc


def unpack_bar_map(bar_info, label_width):
    """
    unpack the bar tuple
    bar_info: (barcode object, desc)
    """
    barcode = bar_info["asset"]
    with tempfile.NamedTemporaryFile(
        prefix=f"{barcode.get_fullcode()}-barcode-", suffix=".png", delete=False
    ) as temp_bar:
        barcode.write(
            temp_bar,
            options={
                "write_text": False,
                "quiet_zone": 0,
                "margin_top": 0,
                "margin_bottom": 0,
            },
        )
        __temp_bar_img = Image.open(temp_bar)
        bar_aspect_ratio = __temp_bar_img.size[1] / __temp_bar_img.size[0]
        __temp_bar_img = __temp_bar_img.resize(
            (
                label_width,
                int(label_width * bar_aspect_ratio),
            )  # basically just the width of the label
        )
        size = __temp_bar_img.size
        desc = desc_builder(bar_info)
        return __temp_bar_img, size, desc


def unpack_title_map(text_info, label_width):
    """
    unpack the title tuple
    same as text but no description
    text_info: (font object, string, desc)
    """
    font = text_info["asset"]
    label_string = text_info["label_text"]
    font_mask = font.getmask(label_string, start=(0, 0))
    # (_, font_descent) = font.getmetrics()
    # size_without_descent = (font_mask.size[0], font_mask.size[1] + font_descent)
    __temp_text_img = Image.frombytes(
        font_mask.mode,
        font_mask.size,
        bytes([255 - byte for byte in bytes(font_mask)]),
    )
    text_aspect_ratio = __temp_text_img.size[1] / __temp_text_img.size[0]
    __temp_text_img = __temp_text_img.resize(
        (
            label_width,
            int(label_width * text_aspect_ratio),
        )  # basically just the width of the label
    )
    size = __temp_text_img.size
    return __temp_text_img, size, None


def unpack_text_map(text_info, label_width):
    """
    unpack the text tuple
    text_info: (font object, string, desc)
    """
    font = text_info["asset"]
    label_string = text_info["label_text"]
    font_mask = font.getmask(label_string, start=(0, 0))
    # (_, font_descent) = font.getmetrics()
    # size_without_descent = (font_mask.size[0], font_mask.size[1] + font_descent)
    __temp_text_img = Image.frombytes(
        font_mask.mode,
        font_mask.size,
        bytes([255 - byte for byte in bytes(font_mask)]),
    )
    text_aspect_ratio = __temp_text_img.size[1] / __temp_text_img.size[0]
    __temp_text_img = __temp_text_img.resize(
        (
            label_width,
            int(label_width * text_aspect_ratio),
        )  # basically just the width of the label
    )
    size = __temp_text_img.size

    desc = desc_builder(text_info)
    return __temp_text_img, size, desc


def desc_builder(info):
    desc = ""
    for i in range(1, len(info)):
        cat, dsc = list(info.items())[i]
        desc += f"{cat}: {dsc} | "
    return desc[:-3]


def arrange_label(
    element_map: dict[int, tuple],
    element_fn_map: list[int, object, object],
    element_regions_map: dict[int, int],
    label_map: dict[int, str],
    regions: dict[int, list],
    element_resizable_map: dict[int, bool],
    margins: tuple[int],
    alignment: str,
) -> dict[int, tuple[int]]:
    """
    element_fn_map: [pos, gen_fn, unpack_fn]

    Open a new bg image baesd on label_size_pix

    Take the positions defined in the label map
    Unpack the correct asset at that position using element_map

    Place the assets onto the bg image
    resize iteratively according to element_resizable

    return the coords of each asset for pdf and zpl generation

    element map is always {pos: (object, config info, desc)}
    """
    # Map of every image to its indexed position
    img_coords_map = {}
    # Map of every description to the indexed position
    desc_map = {}

    """
    sort everything again!? i know this is triple checking at this point
    but we really want to make sure that the indexes line up
    """
    element_fn_map = dict(sorted(element_fn_map.items()))
    element_map = dict(sorted(element_map.items()))
    element_resizable_map = dict(sorted(element_resizable_map.items()))
    element_regions_map = dict(sorted(element_regions_map.items()))
    """
    Does a virtual placing of imgs to coords, so we resize virtually
    without needing to repaste images
    """

    clustered_regions = _cluster_regions(element_regions_map)
    # so we can add margins after resizing
    for r_key, ele_keys in clustered_regions.items():
        # remove margins first, get a dict of pos index: label width
        region_width = regions[r_key]["size"][0] - (margins[0] * 2)
        region_height = regions[r_key]["size"][1]
        region_offset = (regions[r_key]["xyxy"][0], regions[r_key]["xyxy"][1])
        local_element_map = {
            i: asset for i, asset in element_map.items() if i in ele_keys
        }
        local_element_fn_map = {
            i: fns for i, fns in element_fn_map.items() if i in ele_keys
        }
        local_img_coords_map = {}
        for img_coords_pair, desc_coords_pair in unpack_and_gen_coord_maps(
            local_element_map, local_element_fn_map, region_width, margins
        ):
            if desc_coords_pair is not None:
                local_img_coords_map.update(img_coords_pair)
                desc_map.update(desc_coords_pair)
            else:
                # check endpoint of final image for over/underflow
                y_delta = img_coords_pair[1] - region_height
                local_img_coords_map = smart_resize(
                    local_img_coords_map,
                    element_resizable_map,
                    element_fn_map,
                    label_map,
                    y_delta,
                    margins,
                    region_height,
                )
        local_img_coords_map = _align(alignment, local_img_coords_map, region_width)
        local_img_coords_map = _apply_offset(local_img_coords_map, region_offset)
        img_coords_map.update(local_img_coords_map)

    img_coords_map = dict(sorted(img_coords_map.items()))
    return img_coords_map, desc_map


def _align(align_type, map, region_width):
    match align_type:
        case "left":
            _map = {
                i: (_ia, (0, _seed[1]), _sz) for i, (_ia, _seed, _sz) in map.items()
            }
        case "center":
            _map = map
        case "right":
            _map = {
                i: (_ia, (region_width - _sz[0], _seed[1]), _sz)
                for i, (_ia, _seed, _sz) in map.items()
            }
    return _map


def _cluster_regions(_erm):
    # get back a one-time use region: elements dict
    clustered = {}
    for e, r in _erm.items():
        if r not in clustered.keys():
            clustered[r] = []
        clustered[r].append(e)
    return clustered


def _apply_offset(map, xy_offset):
    _map = {
        i: (_ia, (_seed[0] + xy_offset[0], _seed[1] + xy_offset[1]), _sz)
        for i, (_ia, _seed, _sz) in map.items()
    }
    return _map


def unpack_and_gen_coord_maps(
    element_map: dict, element_fn_map: dict, region_width: int, margins: tuple[int, int]
):
    """
    generates bboxes of all assets
    follows pillow's (left, top, right, bottom) standard

    takes the element_regions and places them within those regions
    """
    current_coord = [0, margins[1]]
    for (pos, (_, fn)), (pos, element) in zip(
        element_fn_map.items(), element_map.items()
    ):
        # unpack the objects
        img_asset, size, desc = fn(element, region_width)
        yield {pos: (img_asset, tuple(current_coord), size)}, {pos: desc}
        current_coord = _step_coord(size, current_coord, margins)
    _step_coord(size, current_coord, margins)
    yield tuple(current_coord), None  # end coords for virtual map


def _step_coord(
    size: tuple[int, int], current_coord: list[int, int], margins: tuple[int, int]
):
    current_coord = [current_coord[0], current_coord[1] + size[1] + margins[1]]
    return current_coord


def smart_resize(
    img_coords_map: dict[int, tuple[int]],
    element_resizable_map: dict[int, bool],
    element_fn_map: list[int, object, object],
    label_map: dict[int, str],
    y_delta: int,
    margins: tuple[int, int],
    region_height: int,
) -> dict[int, tuple[int]]:
    """
    Not that smart, just checks for height overflow and adjusts the
    elements if allowed by element_resizable_map

    uses the img_coords_map to find out if barcode/text, to peform
    crop/resize. all img manipulation is done by relative height
    to total sum of all resizable heights

    shifts around image seeds to center all x and y coords w margins

    performs this on each region
    """
    if len(img_coords_map) == 1 and img_coords_map.get(0):
        return img_coords_map

    resizable_imgs = {
        pos: (img_asset, seed, size)
        for pos, (img_asset, seed, size) in img_coords_map.items()
        if element_resizable_map.get(pos)
    }

    rel_reduction = get_relative_scale(resizable_imgs, label_map, y_delta)
    for pos, ((img_asset, seed, size), reduction) in zip(
        resizable_imgs.keys(), zip(resizable_imgs.values(), rel_reduction)
    ):
        # check if qr, bar, text
        match element_fn_map.get(pos)[0].__name__:
            # rescale the image if its too large
            case "gen_qr":
                pass  # intentional
            case "gen_barcode":
                img_asset = img_asset.crop((0, 0, size[0], size[1] - reduction))
                resizable_imgs.update({pos: (img_asset, seed, img_asset.size)})
            case "gen_font" | "gen_title":
                scale_factor = (size[1] - reduction) / size[1]
                img_asset = img_asset.resize(
                    (
                        int(size[0] * scale_factor),
                        int(size[1] * scale_factor),
                    )
                )
                # shift x coord if resized
                x_offset = int((size[0] - (size[0] * scale_factor)) // 2)
                new_x_seed = (seed[0] + x_offset, seed[1])
                resizable_imgs.update({pos: (img_asset, new_x_seed, img_asset.size)})
    for pos, (img_asset, affected_x_seed, affected_size) in resizable_imgs.items():
        if img_coords_map.get(pos - 1) is None:
            # if resizable imgs not included in local region, skip
            img_coords_map.update({pos: (img_asset, affected_x_seed, affected_size)})
            continue
        new_y_coord = (
            img_coords_map.get(pos - 1)[1][1]
            + img_coords_map.get(pos - 1)[2][1]
            + margins[1]
        )  # original y coord + dynamic y size + y margin
        new_y_seed = (affected_x_seed[0], new_y_coord)
        img_coords_map.update({pos: (img_asset, new_y_seed, affected_size)})

    _, last_seed, last_size = img_coords_map.get(max(img_coords_map.keys()))
    new_y_offset = (region_height - last_seed[1] - last_size[1]) // 2 - margins[1]
    if new_y_offset > 0:  # no resize needed, just y coord shift
        img_coords_map = shift_y_coords(img_coords_map, new_y_offset)
    return img_coords_map


def shift_y_coords(
    img_coords_map: dict[int, tuple[int]], shift_delta: int
) -> dict[int, tuple[int]]:
    copy_img_coords = img_coords_map.copy()
    # (k := next(iter(copy_img_coords)), copy_img_coords.pop(k))
    for pos, (img_asset, seed, size) in copy_img_coords.items():
        new_seed = (seed[0], seed[1] + shift_delta)
        img_coords_map.update({pos: (img_asset, new_seed, size)})
    return img_coords_map


def get_relative_scale(
    resizable_imgs: dict[int, tuple[int]], label_map: dict[int, str], y_delta: int
) -> list[int]:
    # larger the image, larger the reduction
    # we want an end result with similar
    if y_delta < 0:
        y_delta = 0
    if y_delta >= 0:
        _text_heights = [
            size[1]
            for i, (_, _, size) in resizable_imgs.items()
            if (label_map[i] in ("text", "title"))
        ]
        _bar_heights = [
            size[1]
            for i, (_, _, size) in resizable_imgs.items()
            if label_map[i] == "bar"
        ]
        fitted_total_height = sum(_text_heights) + sum(_bar_heights) - y_delta
        if _text_heights:
            # bias towards text heights
            ideal_indiv_text_height = min(_text_heights)
            ideal_indiv_bar_height = ideal_indiv_text_height * 2
        else:
            ideal_indiv_text_height = 0
            ideal_indiv_bar_height = min(_bar_heights)
        # the best outcome is to follow the smallest font
        # we want our bar heights to be twice text heights for scannability
        ideal_total_height = ideal_indiv_text_height * len(
            _text_heights
        ) + ideal_indiv_bar_height * len(_bar_heights)
        if (x := fitted_total_height / ideal_total_height) < 1:
            # if still greater than fitted height, scale towards lower one
            ideal_indiv_bar_height *= x
            ideal_indiv_text_height *= x
        scaling_factors = []
        for pos, (_, _, size) in resizable_imgs.items():
            if label_map[pos] in ("text", "title"):
                scaling_factors.append(ideal_indiv_text_height / size[1])
            elif label_map[pos] == "bar":
                scaling_factors.append(ideal_indiv_bar_height / size[1])
        # ensure no upscaling
        scaling_factors = [min(1, factor) for factor in scaling_factors]

        # total_scaling_factor = sum(scaling_factors)
        # normalized_scaling_factors = [
        #     factor / total_scaling_factor for factor in scaling_factors
        # ]
        individual_y_resize_reduction = [
            int(size[1] * (1 - factor))
            for factor, (_, _, size) in zip(scaling_factors, resizable_imgs.values())
        ]
        return individual_y_resize_reduction


def gen_to_list(gen_fn: object) -> list:
    def get_list(*args, **kwargs):
        gen_obj = gen_fn(*args, **kwargs)
        return list(gen_obj)

    return get_list


@gen_to_list
def gen_labels(img_coords_maps, label_size_pix, margins):
    """
    Paste everything!
    """
    for img_coords_map in img_coords_maps:
        with tempfile.NamedTemporaryFile(
            prefix=f"label", suffix=".png", delete=False
        ) as temp_label:
            __temp_bg_img = Image.new(mode="L", size=label_size_pix, color=(255))
            for _, (img_asset, seed, _) in img_coords_map.items():
                seed = (seed[0] + margins[0], seed[1])
                __temp_bg_img.paste(img_asset, seed)

            __temp_bg_img.save(temp_label)
            yield temp_label


def gen_bg(label_string: str, label_size: tuple[int, int]):
    with tempfile.NamedTemporaryFile(
        prefix=f"{label_string}-bg-", suffix=".png", delete=False
    ) as temp_bg:
        label_bg = Image.new(mode="L", size=label_size, color=(255))  # 203PPI, 3x4in
        label_bg.save(temp_bg)
        return temp_bg


def auto_qr_sizing(label_string, region_size):
    qr = segno.make(label_string, micro=False)
    module_size = 1
    jumpsize = 5
    while True:
        if qr.symbol_size(scale=module_size, border=1)[0] < region_size[0]:
            module_size += jumpsize
        else:
            jumpsize -= 1
            module_size -= jumpsize
        if jumpsize <= 1:
            module_size += 1
            break
    return qr, module_size


def auto_font(font_path: str, label_string: str, region_size: object) -> object:
    font = ImageFont.truetype(font_path, 1)
    breakpoint = region_size[0] - (region_size[0] / 15)
    jumpsize = 50
    fontsize = 1
    while True:
        if font.getlength(label_string) < breakpoint:
            fontsize += jumpsize
        else:
            jumpsize //= 2
            fontsize -= jumpsize
        font = ImageFont.truetype(font_path, fontsize)
        if jumpsize <= 1:
            break
    return font, fontsize
