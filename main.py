import matplotlib.pyplot as plt
from rectpack import SORT_AREA, SORT_LSIDE, newPacker
from rectpack import GuillotineBlsfSas as Algorithm
from rectpack.geometry import Rectangle

# from rectpack import GuillotineBssfSas # cross - good
# from rectpack import GuillotineBlsfSas # rip - good
# from rectpack import GuillotineBlsfMaxas # same as GuillotineBlsfSas
# from rectpack import GuillotineBafSas # same as GuillotineBlsfSas


# -----------------------------
# CONFIGURATION
# -----------------------------
# Panel dimensions (cm)
PANELS = [
    # LENGTH, WIDTH, COUNT
    (200, 60, 4),
    (200, 40, 2),
    # Missing:
    (200, 50, 1),
    # Drawer Bottoms
    # (120, 60, 4),
]
PANEL_LENGTH = 240
PANEL_WIDTH = 40
PANEL_THICKNESS = 1.8

# Saw margin (cm)
CUT_MARGIN = 1

BODY_WIDTH = 116
BODY_DEPTH = 50
BODY_HEIGHT = 110

DRAWER_SPACER_WIDTH = BODY_DEPTH - (2 * PANEL_THICKNESS)
TOP_DRAWER_SPACER_HEIGHT = 7
DRAWER_SPACER_HEIGHT = 5
BOTTOM_DRAWER_SPACER_HEIGHT = 8

DRAWER_DEPTH = 55
DRAWER_HEIGHT = 19
DRAWER_WIDTH = 46

DRAWER_BOX_FRONT_HEIGHT = DRAWER_HEIGHT
DRAWER_BOX_FRONT_WIDTH = DRAWER_WIDTH
DRAWER_BOX_BACK_HEIGHT = DRAWER_HEIGHT - 1.5
DRAWER_BOX_BACK_WIDTH = DRAWER_WIDTH
DRAWER_BOX_SIDE_HEIGHT = DRAWER_HEIGHT
DRAWER_BOX_SIDE_WIDTH = DRAWER_DEPTH

DRAWER_BOTTOM_DEPTH = 43
DRAWER_BOTTOM_WIDTH = 54

DRAWER_FRONT_WIDTH = 50
DRAWER_FRONT_HEIGHT = 22


# -----------------------------
# DATA CLASSES
# -----------------------------
class PanelPiece:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width
        self.thickness = PANEL_THICKNESS


# -----------------------------
# EXAMPLE PIECES
# -----------------------------
panel_pieces = [
    # BODY
    PanelPiece("Side Half 1", BODY_WIDTH, BODY_HEIGHT / 2),
    PanelPiece("Side Half 2", BODY_WIDTH, BODY_HEIGHT / 2),
    PanelPiece("Side Half 3", BODY_WIDTH, BODY_HEIGHT / 2),
    PanelPiece("Side Half 4", BODY_WIDTH, BODY_HEIGHT / 2),
    PanelPiece("Top Drawer Spacer 1", DRAWER_SPACER_WIDTH, TOP_DRAWER_SPACER_HEIGHT),
    PanelPiece("Top Drawer Spacer 2", DRAWER_SPACER_WIDTH, TOP_DRAWER_SPACER_HEIGHT),
    PanelPiece("Drawer Spacer 1", DRAWER_SPACER_WIDTH, DRAWER_SPACER_HEIGHT),
    PanelPiece("Drawer Spacer 2", DRAWER_SPACER_WIDTH, DRAWER_SPACER_HEIGHT),
    PanelPiece("Drawer Spacer 3", DRAWER_SPACER_WIDTH, DRAWER_SPACER_HEIGHT),
    PanelPiece("Drawer Spacer 4", DRAWER_SPACER_WIDTH, DRAWER_SPACER_HEIGHT),
    PanelPiece("Drawer Spacer 5", DRAWER_SPACER_WIDTH, DRAWER_SPACER_HEIGHT),
    PanelPiece("Drawer Spacer 6", DRAWER_SPACER_WIDTH, DRAWER_SPACER_HEIGHT),
    PanelPiece("Bottom Drawer Spacer 1", DRAWER_SPACER_WIDTH, BOTTOM_DRAWER_SPACER_HEIGHT),
    PanelPiece("Bottom Drawer Spacer 2", DRAWER_SPACER_WIDTH, BOTTOM_DRAWER_SPACER_HEIGHT),
    # DRAWERS
    PanelPiece("Drawer Box Front 1", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Front 2", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Front 3", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Front 4", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Front 5", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Front 6", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Front 7", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Front 8", DRAWER_BOX_FRONT_WIDTH, DRAWER_BOX_FRONT_HEIGHT),
    PanelPiece("Drawer Box Back 1", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Back 2", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Back 3", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Back 4", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Back 5", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Back 6", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Back 7", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Back 8", DRAWER_BOX_BACK_WIDTH, DRAWER_BOX_BACK_HEIGHT),
    PanelPiece("Drawer Box Side 1", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 2", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 3", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 4", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 5", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 6", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 7", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 8", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 9", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 10", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 11", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 12", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 13", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 14", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 15", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    PanelPiece("Drawer Box Side 16", DRAWER_BOX_SIDE_WIDTH, DRAWER_BOX_SIDE_HEIGHT),
    # DRAWER BOTTOMS
    # PanelPiece("Drawer Bottom 1", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
    # PanelPiece("Drawer Bottom 2", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
    # PanelPiece("Drawer Bottom 3", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
    # PanelPiece("Drawer Bottom 4", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
    # PanelPiece("Drawer Bottom 5", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
    # PanelPiece("Drawer Bottom 6", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
    # PanelPiece("Drawer Bottom 7", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
    # PanelPiece("Drawer Bottom 8", DRAWER_BOTTOM_WIDTH, DRAWER_BOTTOM_DEPTH),
]


# -----------------------------
# PANEL PACKING
# -----------------------------
def pack_panel(pieces: list[PanelPiece]) -> list[tuple[float, float, list[tuple[str, float, float, float, float]]]]:
    packer = newPacker(rotation=False, sort_algo=SORT_AREA, pack_algo=Algorithm)

    # Add pieces
    for piece in pieces:
        packer.add_rect(piece.length + CUT_MARGIN, piece.width + CUT_MARGIN, rid=piece.name)

    # Add panel bin
    for panel in PANELS:
        packer.add_bin(*panel)

    packer.pack()
    if not packer:
        raise Exception("Nothing fits")

    # Collect packed pieces
    packed_rids = {rect.rid for rects in packer for rect in rects}

    # Find unplaced pieces
    unplaced = [piece.name for piece in pieces if piece.name not in packed_rids]
    if unplaced:
        print("⚠️  These pieces did not fit in any panel:")
        for name in unplaced:
            print(f"  - {name}")

    placements = []
    panels = packer.bin_list()
    for bin_index, rectangles in enumerate(packer):
        panel = panels[bin_index]
        panel_placements = []
        for rect in rectangles:
            x = rect.x
            y = rect.y
            w = rect.width
            h = rect.height
            rid = rect.rid
            panel_placements.append((rid, x, y, w, h))
        placements.append((panel[0], panel[1], panel_placements))
    # Find unplaced rectangles
    unplaced = [r[2] for r in packer.rect_list() if r[-1] is None]
    if unplaced:
        print("⚠️ These pieces did not fit in any panel:")
        for name in unplaced:
            print(f"  - {name}")
    return placements


# -----------------------------
# VISUALIZATION
# -----------------------------
def draw_panel(placements: list[tuple[str, float, float, float, float]], panel_l: float, panel_w: float):
    fig, ax = plt.subplots(figsize=(11, 5))
    plt.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.03)
    ax.set_xlim(0, panel_l)
    ax.set_ylim(0, panel_w)
    ax.set_aspect("equal")
    ax.set_title("Panel Cut Plan")

    # Draw panel border
    ax.add_patch(plt.Rectangle((0, 0), panel_l, panel_w, fill=False, edgecolor="black", linewidth=2))

    # Draw pieces with grain direction (hatch = /// along panel length)
    for rid, x, y, w, h in placements:
        rect = plt.Rectangle(
            (x, y), w, h, fill=True, edgecolor="darkgoldenrod", facecolor="burlywood", hatch="---", alpha=0.4
        )
        ax.add_patch(rect)
        true_w = w - CUT_MARGIN
        true_h = h - CUT_MARGIN
        ax.text(x + w / 2, y + h / 2 - 0.5, rid, ha="center", va="center", fontsize=12, weight="roman")
        ax.text(x + w / 2, y + h / 2 + 2, f"({true_w:.1f} × {true_h:.1f} cm)", ha="center", va="center", fontsize=8)
    plt.gca().invert_yaxis()  # so origin is top-left


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    placements = pack_panel(panel_pieces)
    for panel_l, panel_w, panel_placements in placements:
        draw_panel(panel_placements, panel_l, panel_w)
    plt.show()
