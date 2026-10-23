import argparse
import importlib.util
from pathlib import Path

from classes import Bin, Shape


def get_config_path() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("work_file", help="Path to the work configuration, relative to the project root")
    args = parser.parse_args()

    project_root: Path = Path(__file__).resolve().parent
    config_path: Path = (project_root / args.work_file).resolve()
    return config_path


def load_work_config(config_path: Path) -> tuple[list[Shape], list[Bin]]:
    """
    Load shapes and bins from a Python configuration file.
    by: ChatGPT
    """
    config_path = config_path.resolve()

    spec = importlib.util.spec_from_file_location("work_config", config_path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load config: {config_path}")

    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    # Check that the expected parameters exist
    if not hasattr(config, "shapes"):
        raise ValueError("Config must define 'shapes'")

    if not hasattr(config, "bins"):
        raise ValueError("Config must define 'bins'")

    return config.shapes, config.bins
