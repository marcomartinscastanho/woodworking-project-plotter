# -----------------------------
# VISUALIZATION
# -----------------------------
import matplotlib.pyplot as plt

from config import CUT_MARGIN


def draw_panel(placements: list[tuple[str, float, float, float, float]], panel_l: float, panel_w: float):
    _, ax = plt.subplots(figsize=(11, 5))
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
