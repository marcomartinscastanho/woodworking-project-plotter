from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from loader import get_config_path, load_work_config
from packing import pack_panel
from visualization import draw_panel


def main():
    config_path = get_config_path()
    work_dir: Path = config_path.parent
    work_name: str = config_path.stem

    shapes, bins = load_work_config(config_path)

    print("Shapes:", *shapes, sep="\n")
    print("Bins:", *bins, sep="\n")

    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = work_dir / f"{work_name}_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Algorithms:
    # from rectpack import GuillotineBssfSas # cross -> good
    # from rectpack import GuillotineBlsfSas # rip -> good
    placements = pack_panel(bins, shapes)
    for i, (panel_l, panel_w, panel_placements) in enumerate(placements, start=1):
        draw_panel(panel_placements, panel_l, panel_w)
        output_path = output_dir / f"{i}.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
