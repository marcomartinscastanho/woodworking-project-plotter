import matplotlib.pyplot as plt
from rectpack import SORT_LSIDE, newPacker
from rectpack import GuillotineBssfSas as Algorithm
from rectpack.geometry import Rectangle

# from rectpack import GuillotineBssfSas # cross - good
# from rectpack import GuillotineBlsfSas # rip - good
# from rectpack import GuillotineBlsfMaxas # same as GuillotineBlsfSas
# from rectpack import GuillotineBafSas # same as GuillotineBlsfSas


# -----------------------------
# CONFIGURATION
# -----------------------------
# Panel dimensions (cm)
PANEL_LENGTH = 240
PANEL_WIDTH = 60
PANEL_THICKNESS = 1.8

# Beam dimensions (cm)
BEAM_WIDTH = 5.0
BEAM_HEIGHT = 7.0

# Saw margin (cm)
CUT_MARGIN = 1.0

# Sofa dimensions
SOFA_WIDTH = 164
SOFA_HEIGHT = 64
# Baseboard
BASEBOARD_HEIGHT = 7.5
BASEBOARD_DEPTH = 1.5
# PIECE
PIECE_WIDTH = SOFA_WIDTH  # 164
PIECE_HEIGHT = SOFA_HEIGHT  # 64
PIECE_DEPTH = 14
# BOX
BOX_INNER_DEPTH = 16
BOX_INNER_WIDTH = PIECE_DEPTH - (2 * PANEL_THICKNESS)


# -----------------------------
# DATA CLASSES
# -----------------------------
class PanelPiece:
    def __init__(self, name, length, width):
        self.name = name
        self.length = length
        self.width = width
        self.thickness = PANEL_THICKNESS


class BeamPiece:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.width = BEAM_WIDTH
        self.height = BEAM_HEIGHT


# -----------------------------
# EXAMPLE PIECES
# -----------------------------
panel_pieces = [
    PanelPiece("Prancha", PIECE_WIDTH, PIECE_DEPTH),
    PanelPiece("Topo 1", PIECE_WIDTH / 2, PIECE_DEPTH),
    PanelPiece("Topo 2", PIECE_WIDTH / 2, PIECE_DEPTH),
    PanelPiece("Chão 1", BOX_INNER_DEPTH + PANEL_THICKNESS, PIECE_DEPTH - BASEBOARD_DEPTH),
    PanelPiece("Chão 1", BOX_INNER_DEPTH + PANEL_THICKNESS, PIECE_DEPTH - BASEBOARD_DEPTH),
    PanelPiece("Prateleira 1", BOX_INNER_DEPTH + (PANEL_THICKNESS / 2), BOX_INNER_WIDTH + PANEL_THICKNESS),
    PanelPiece("Prateleira 2", BOX_INNER_DEPTH + (PANEL_THICKNESS / 2), BOX_INNER_WIDTH + PANEL_THICKNESS),
    PanelPiece("Fundo 1", PIECE_HEIGHT - (3 * PANEL_THICKNESS), PIECE_DEPTH),
    PanelPiece("Fundo 2", PIECE_HEIGHT - (3 * PANEL_THICKNESS), PIECE_DEPTH),
    PanelPiece("Laterais Sofá 1", PIECE_HEIGHT - (3 * PANEL_THICKNESS), BOX_INNER_DEPTH),
    PanelPiece("Laterais Sofá 2", PIECE_HEIGHT - (3 * PANEL_THICKNESS), BOX_INNER_DEPTH),
    PanelPiece("Laterais Parede 1", PIECE_HEIGHT - (2 * PANEL_THICKNESS) - BASEBOARD_HEIGHT, BOX_INNER_DEPTH),
    PanelPiece("Laterais Parede 2", PIECE_HEIGHT - (2 * PANEL_THICKNESS) - BASEBOARD_HEIGHT, BOX_INNER_DEPTH),
]

beam_pieces = [
    BeamPiece("Barrote H 1", (PIECE_WIDTH / 2) - BOX_INNER_DEPTH),
    BeamPiece("Barrote H 2", (PIECE_WIDTH / 2) - BOX_INNER_DEPTH),
    BeamPiece("Barrote V 1", PIECE_HEIGHT - BEAM_HEIGHT - PANEL_THICKNESS),
    BeamPiece("Barrote V 2", PIECE_HEIGHT - BEAM_HEIGHT - PANEL_THICKNESS),
]


# -----------------------------
# BEAM REQUIREMENT CHECK
# -----------------------------
def total_beam_length(pieces: list[BeamPiece]):
    return sum(p.length for p in pieces)


# -----------------------------
# PANEL PACKING
# -----------------------------
def pack_panel(pieces: list[PanelPiece], panel_l: float, panel_w: float, margin: float):
    packer = newPacker(rotation=False, sort_algo=SORT_LSIDE, pack_algo=Algorithm)

    # Add pieces
    for piece in pieces:
        packer.add_rect(piece.length + margin, piece.width + margin, rid=piece.name)

    # Add panel bin
    packer.add_bin(panel_l, panel_w)

    packer.pack()

    if not packer:
        return None  # nothing fit

    placements = []
    rectangles: list[Rectangle] = packer[0]
    for rect in rectangles:
        # print("rect:", rect)
        # x, y, w, h = rect
        x = rect.x
        y = rect.y
        w = rect.width
        h = rect.height
        rid = rect.rid
        placements.append((rid, x, y, w, h))

    if len(placements) < len(pieces):
        return None  # not all pieces fit
    return placements


# -----------------------------
# VISUALIZATION
# -----------------------------
def draw_panel(placements, panel_l, panel_w):
    fig, ax = plt.subplots()
    ax.set_xlim(0, panel_l)
    ax.set_ylim(0, panel_w)
    ax.set_aspect("equal")
    ax.set_title("Panel Cut Plan (Grain shown)")

    # Draw panel border
    ax.add_patch(plt.Rectangle((0, 0), panel_l, panel_w, fill=False, edgecolor="black", linewidth=2))

    # Draw pieces with grain direction (hatch = /// along panel length)
    for rid, x, y, w, h in placements:
        rect = plt.Rectangle(
            (x, y),
            w,
            h,
            fill=True,
            edgecolor="darkgoldenrod",
            facecolor="burlywood",
            hatch="---",  # shows grain direction
            alpha=0.4,
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, rid, ha="center", va="center", fontsize=12, weight="roman")

    plt.gca().invert_yaxis()  # so origin is top-left
    plt.show()


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("Panel pieces:")
    for p in panel_pieces:
        print(f"  {p.name}: {p.length} × {p.width} cm")

    print("\nBeam pieces:")
    for b in beam_pieces:
        print(f"  {b.name}: {b.length} cm")

    total_beam = total_beam_length(beam_pieces)
    print(f"\nTotal beam length required: {total_beam} cm")

    placements = pack_panel(panel_pieces, PANEL_LENGTH, PANEL_WIDTH, CUT_MARGIN)

    if placements:
        print("\nPanel cut plan is possible.")
        for rid, x, y, w, h in placements:
            print(f"  {rid} at ({x:.1f},{y:.1f}), size {w:.1f}×{h:.1f}")
        draw_panel(placements, PANEL_LENGTH, PANEL_WIDTH)
    else:
        print("\nPanel cut plan NOT possible with given dimensions.")
