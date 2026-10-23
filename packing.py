from rectpack import SORT_AREA, GuillotineBlsfSas, newPacker

from classes import Bin, Shape
from config import CUT_MARGIN


def pack_panel(
    bins: list[Bin], shapes: list[Shape], Algorithm: type[GuillotineBlsfSas] = GuillotineBlsfSas
) -> list[tuple[float, float, list[tuple[str, float, float, float, float]]]]:
    packer = newPacker(rotation=False, sort_algo=SORT_AREA, pack_algo=Algorithm)

    # Add pieces
    for shape in shapes:
        packer.add_rect(shape.length + CUT_MARGIN, shape.width + CUT_MARGIN, rid=shape.name)

    # Add panel bin
    for bin in bins:
        packer.add_bin(*bin)

    packer.pack()
    if not packer:
        raise Exception("Nothing fits")

    # Collect packed pieces
    packed_rids = {rect.rid for rects in packer for rect in rects}

    # Find unplaced pieces
    unplaced = [shape.name for shape in shapes if shape.name not in packed_rids]
    if unplaced:
        print("⚠️  These pieces did not fit in any panel:")
        for name in unplaced:
            print(f"  - {name}")

    placements = []
    panels = packer.bin_list()
    for bin_index, rectangles in enumerate(packer):
        bin = panels[bin_index]
        panel_placements = []
        for rect in rectangles:
            x = rect.x
            y = rect.y
            w = rect.width
            h = rect.height
            rid = rect.rid
            panel_placements.append((rid, x, y, w, h))
        placements.append((bin[0], bin[1], panel_placements))
    # Find unplaced rectangles
    unplaced = [r[2] for r in packer.rect_list() if r[-1] is None]
    if unplaced:
        print("⚠️ These pieces did not fit in any panel:")
        for name in unplaced:
            print(f"  - {name}")
    return placements
